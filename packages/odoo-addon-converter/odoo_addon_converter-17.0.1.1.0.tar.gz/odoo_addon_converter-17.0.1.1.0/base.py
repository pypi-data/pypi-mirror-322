##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020 XCG Consulting <https://xcg-consulting.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Converter is a utility class that makes conversion very easy between
Odoo records & JSON dicts. It's very fast and extendable and convert both ways.

Supports aggregates of the form (simplified example JSON-schemas)::
    {"type": "object", "properties": { "items": { "type": "array", "items": {
        "type": "object", "properties": {
            "data": {"oneOf": [{"$ref": "user.json"}, {"$ref": "s2.json"}]}
        }
    }}}}
    ---
    {"$id": "user.json", "type": "object", "properties": {
        "__type__": {"type": "string", "enum": ["user"]},
        "name": {"type": "string"}
    }}
"""

import inspect
import logging
from collections.abc import Callable, Mapping
from typing import Any

from odoo import api, models

from .exception import InternalError
from .validate import Validator

logger = logging.getLogger(__name__)


class SkipType:
    pass


Skip = SkipType()


class NewinstanceType:
    pass


Newinstance = NewinstanceType()

ContextBuilder = Callable[[models.Model, Mapping | None], Mapping | None]

PHASE_PRECREATE = "precreate"
PHASE_POSTCREATE = "postcreate"
PHASE_UPDATE = "UPDATE"

OPERATION_CREATION = "create"
OPERATION_UPDATE = "update"


def build_context(
    instance: models.Model | None,
    ctx: Mapping | None,
    extend: ContextBuilder | None,
) -> dict | None:
    if instance is None:
        return ctx
    if extend:
        if ctx is None:
            ctx = {}
        else:
            ctx = dict(ctx)
        ctx.update(extend(instance))
    return ctx


class Converter:
    """Base converter class.
    It does not actually convert anything.
    """

    def odoo_to_message(
        self, instance: models.Model, ctx: Mapping | None = None
    ) -> Any:
        """From an instance, this method returns a matching value for the
        message field.
        :param instance: an instance of an Odoo model
        :param ctx: context value
        :return: The value or Skip if not included in the message.
        """
        return Skip

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.Model,
        value_present: bool = True,
    ) -> dict:
        """From a message, returns a dict.
        Only field whose values are changed are included in the returned dict.
        :param odoo_env: odoo environment
        :param phase: precreate, postcreate, update
        :param message_value: the value of the message
        :param instance: an odoo instance, used to remove existing value from
        the produced dict as needed
        :param value_present: indicate if the value was actually in the message
        (in order to differentiate given None values to non provided values)
        :return: dict of changes to apply on an instance (if any).
        """
        return {}

    @classmethod
    def is_instance_getter(cls) -> bool:
        return False

    def get__type__(self) -> set[str]:
        """Indicate if this converter is associated to several __type__.
        If so, it will be called with incoming messages associated to them.
        (using message_to_odoo)"""
        return set()

    @property
    def validator(self) -> Validator | None:
        """A validator to use for validation of created messages"""
        return self._validator

    @validator.setter
    def validator(self, value: Validator | None) -> None:
        if value is None:
            self._validator = None
        else:
            if value.initialized:
                self._validator = value
            else:
                raise InternalError(
                    "you must initialize() the validator before passing it"
                )

    @property
    def validation(self) -> str:
        return self._validation

    @validation.setter
    def validation(self, value: str) -> None:
        """Define if validation should be done"""
        assert value is not None
        self._validation = value


class Readonly(Converter):
    def __init__(self, conv):
        super().__init__()
        self.conv = conv

    def odoo_to_message(self, instance: models.Model, ctx: dict | None = None) -> Any:
        return self.conv.odoo_to_message(instance, ctx)


class Computed(Converter):
    def __init__(self, from_odoo: Callable[[models.Model, Mapping | None], Any]):
        self.from_odoo = from_odoo

        sig = inspect.signature(from_odoo)
        self.from_odoo_arg_count = len(sig.parameters)
        if self.from_odoo_arg_count not in (1, 2):
            raise ValueError(
                "Computed 'from_odoo' callback must have 1 or 2 args: got %s"
                % self.from_odoo_arg_count
            )

    def odoo_to_message(
        self, instance: models.Model, ctx: Mapping | None = None
    ) -> Any:
        if self.from_odoo_arg_count == 1:
            return self.from_odoo(instance)
        return self.from_odoo(instance, ctx)


class Constant(Converter):
    def __init__(self, value):
        self.value = value

    def odoo_to_message(
        self, instance: models.Model, ctx: Mapping | None = None
    ) -> Any:
        return self.value


def message_to_odoo(
    odoo_env: api.Environment,
    payload: Mapping,
    model_name: str,
    converter: Converter,
    operation: str | None = None,
) -> models.Model:
    """

    :param odoo_env: an Odoo environment
    :param payload: received data
    :param model_name: name of an Odoo model
    :param converter:
    :param operation: if operation is not given, creation will be done if no
       instance can be found by using
       :py:meth:odoo.addons.Converter.get_instance
    :return:
    """
    if operation == OPERATION_CREATION:
        instance = Newinstance
    else:
        instance = converter.get_instance(odoo_env, payload)
    if operation == OPERATION_CREATION or (
        operation is None and not instance or instance is Newinstance
    ):
        changes = converter.message_to_odoo(
            odoo_env, PHASE_PRECREATE, payload, instance
        )
        instance = odoo_env[model_name].create(changes)
        changes = converter.message_to_odoo(
            odoo_env, PHASE_POSTCREATE, payload, instance
        )
        if changes:
            instance.write(changes)
    if operation == OPERATION_UPDATE or not (
        operation is None and not instance or instance is Newinstance
    ):
        changes = converter.message_to_odoo(odoo_env, PHASE_UPDATE, payload, instance)
        if changes:
            instance.write(changes)
    if hasattr(converter, "post_hook"):
        converter.post_hook(instance, payload)
    return instance

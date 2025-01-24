##############################################################################
#
#    Converter Odoo module
#    Copyright (C) 2020 XCG Consulting <https://xcg-consulting.fr>
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

import logging
from collections import OrderedDict
from collections.abc import Iterable, Mapping
from typing import Any, Optional

from odoo import api, models

from .base import (
    ContextBuilder,
    Converter,
    Newinstance,
    NewinstanceType,
    Skip,
    build_context,
)
from .validate import VALIDATION_SKIP, VALIDATION_STRICT, Validator

_logger = logging.getLogger(__name__)


class Model(Converter):
    """A converter that takes a dict of key, used when a message has values"""

    def __init__(
        self,
        __type__: str,
        converters: Mapping[str, Converter],
        json_schema: Optional[str] = None,
        # The validator is usually not given at this point but is common
        # throughout a project. That’s why it is a property
        validator: Optional[Validator] = None,
        merge_with: Optional[Iterable[Converter]] = None,
        validation: str = VALIDATION_SKIP,
        context: Optional[ContextBuilder] = None,
    ):
        super().__init__()
        self._type: str = __type__
        self._converters: Mapping[str, Converter] = converters
        self._post_hooks_converters_key: list[str] = []
        self._jsonschema: Optional[str] = json_schema
        self._get_instance: Converter = None
        """First converter whose `is_instance_getter` is true if any"""
        self.merge_with: Optional[Iterable[Converter]] = merge_with
        self.context: Optional[ContextBuilder] = context
        self.validator: Optional[Validator] = validator
        self.validation = validation

        for key, converter in converters.items():
            if self._get_instance is None and converter.is_instance_getter():
                self._get_instance = key
            if hasattr(converter, "post_hook"):
                self._post_hooks_converters_key.append(key)

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[dict] = None
    ) -> Any:
        ctx = build_context(instance, ctx, self.context)

        message_data = {}
        if self._type:
            message_data["__type__"] = self._type

        for key in self._converters:
            value = self._converters[key].odoo_to_message(instance, ctx)
            if value is not Skip:
                message_data[key] = value

        if self.merge_with:
            for conv in self.merge_with:
                value = conv.odoo_to_message(instance, ctx)
                if value is Skip:
                    continue
                message_data.update(value)

        if self.validation != VALIDATION_SKIP and self._jsonschema is not None:
            try:
                self.validator.validate(self._jsonschema, message_data)
            except Exception as exception:
                _logger.warning("Validation failed", exc_info=1)
                if self.validation == VALIDATION_STRICT:
                    raise exception

        return message_data

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.Model,
        value_present: bool = True,
    ) -> dict:
        values = OrderedDict()

        if self._type and message_value["__type__"] != self._type:
            raise Exception(
                "Expected __type__ {}, found {}".format(
                    self._type, message_value["__type__"]
                )
            )
        for key in self._converters:
            value = message_value.get(key, None) if message_value else None
            values.update(
                self._converters[key].message_to_odoo(
                    odoo_env,
                    phase,
                    value,
                    instance,
                    message_value and key in message_value,
                )
            )
        if self.merge_with:
            for conv in self.merge_with:
                value = conv.message_to_odoo(
                    odoo_env, phase, message_value, instance, value_present
                )
                if value is Skip:
                    continue
                values.update(value)

        return values

    def is_instance_getter(self) -> bool:
        return self._get_instance is not None

    def get_instance(
        self, odoo_env: api.Environment, message_data
    ) -> None | models.Model | NewinstanceType:
        """:return: an instance linked to the converter, if any"""
        if self._get_instance:
            instance = self._converters[self._get_instance].get_instance(
                odoo_env, message_data[self._get_instance]
            )
            if instance is None:
                instance = Newinstance
            return instance
        return None

    def post_hook(self, instance: models.Model, message_data):
        for key in self._post_hooks_converters_key:
            if key in message_data:
                self._converters[key].post_hook(instance, message_data[key])
        if self.merge_with:
            for converter in self.merge_with:
                if hasattr(converter, "post_hook"):
                    converter.post_hook(instance, message_data)

    def get__type__(self) -> set[str]:
        return {self._type}

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
import warnings
from typing import Any, Callable, Dict, Optional, Union

from odoo import api, models

from .base import ContextBuilder, Converter, Newinstance, Skip, build_context
from .field import Field

_logger = logging.getLogger(__name__)


class RelationToOne(Field):
    def __init__(
        self,
        field_name: str,
        model_name: str,
        converter: Converter,
        send_empty: bool = True,
        context: Optional[ContextBuilder] = None,
    ):
        super().__init__(field_name)
        self.converter = converter
        self.model_name = model_name
        self._send_empty = send_empty
        self.context = context

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        ctx = build_context(instance, ctx, self.context)
        # do not use super, otherwise if empty, will convert that
        relation_instance = getattr(instance, self.field_name)
        if not relation_instance:
            if not self._send_empty:
                return Skip
            else:
                relation_instance = instance.env[self.model_name]
        return self.converter.odoo_to_message(relation_instance, ctx)

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.Model,
        value_present: bool = True,
    ) -> Dict:
        if not value_present:
            return {}

        post_hook = getattr(self.converter, "post_hook", None)

        if self.converter.is_instance_getter():
            rel_record = self.converter.get_instance(odoo_env, message_value)

            if rel_record is None:
                return {self.field_name: None}

            if rel_record is Newinstance:
                rel_record = None

            updates = self.converter.message_to_odoo(
                odoo_env, phase, message_value, rel_record, value_present
            )

            if updates:
                if rel_record:
                    rel_record.write(updates)
                else:
                    rel_record = odoo_env[self.model_name].create(updates)

                if post_hook:
                    post_hook(rel_record, message_value)

            if instance:
                field_value = getattr(instance, self.field_name)

                if field_value and field_value.id == rel_record.id:
                    return {}
                return {self.field_name: rel_record.id}
            return {self.field_name: rel_record.id}

        else:
            field_value = (
                getattr(instance, self.field_name) if instance else None
            )

            updates = self.converter.message_to_odoo(
                odoo_env, phase, message_value, field_value, value_present
            )

            if updates:
                if field_value:
                    field_value.write(updates)
                    if post_hook:
                        post_hook(field_value, message_value)
                    return {}
                else:
                    rel_record = odoo_env[self.model_name].create(updates)
                    if post_hook:
                        post_hook(rel_record, message_value)
                    return {self.field_name: rel_record.id}
            return {}


class RelationToMany(Field):
    def __init__(
        self,
        field_name: str,
        model_name: Optional[str],
        converter: Converter,
        filtered: Union[None, str, Callable[[models.Model], bool]] = None,
        context: Optional[ContextBuilder] = None,
        limit: Optional[Any] = None,
    ):
        """
        :param filtered: filter to use in Odoo’s BaseModel filtered method.
        """
        super().__init__(field_name)
        self.converter = converter
        self.model_name = model_name
        self.filtered = filtered
        self.context = context
        self.limit = limit

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        ctx = build_context(instance, ctx, self.context)
        value = super().odoo_to_message(instance, ctx)
        if value is Skip:
            return Skip
        if self.filtered:
            value = value.filtered(self.filtered)
        if self.limit:
            value = value[: self.limit]

        return [
            m
            for m in (self.converter.odoo_to_message(r, ctx) for r in value)
            if m is not Skip
        ]

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.Model,
        value_present: bool = True,
    ) -> Dict:
        # if not present or value is None, do not update the values.
        if not value_present or message_value is None:
            return {}
        field_instances = odoo_env[self.model_name]
        for value in message_value:
            field_instances |= odoo_env["ir.model.data"].browseXref(value)
        if instance and getattr(instance, self.field_name) == field_instances:
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


class RelationToManyMap(Field):
    def __init__(
        self,
        field_name: str,
        model_name: Optional[str],
        key_converter: Converter,
        value_converter: Converter,
        filtered: Union[None, str, Callable[[models.Model], bool]] = None,
        context: Optional[ContextBuilder] = None,
    ):
        """
        :param filtered: filter to use in Odoo’s BaseModel filtered method.
        """
        super().__init__(field_name)
        self.key_converter = key_converter
        self.value_converter = value_converter
        self.model_name = model_name
        self.filtered = filtered
        self.context = context

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        ctx = build_context(instance, ctx, self.context)
        value = super().odoo_to_message(instance, ctx)
        if value is Skip:
            return Skip
        if self.filtered:
            value = value.filtered(self.filtered)
        return {
            k: v
            for k, v in (
                (
                    self.key_converter.odoo_to_message(r, ctx),
                    self.value_converter.odoo_to_message(r, ctx),
                )
                for r in value
            )
            if k is not Skip and v is not Skip
        }

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.Model,
        value_present: bool = True,
    ) -> Dict:
        # if not present or value is None, do not update the values.
        if not value_present or message_value is None:
            return {}
        field_instances = odoo_env[self.model_name]
        for value in message_value:
            field_instances |= odoo_env["ir.model.data"].browseXref(value)
        if instance and getattr(instance, self.field_name) == field_instances:
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


def relation(path: str, converter: Converter) -> Converter:
    for name in reversed(path.split("/")):
        model_name = None
        pi = name.find("(")
        if pi != -1:
            if not name.endswith(")"):
                raise ValueError("Invalid path: %s", name)
            model_name = name[pi + 1 : -1]  # noqa: E203
            name = name[:pi]
        if name.endswith("[]"):
            converter = RelationToMany(name[:-2], model_name, converter)
        else:
            converter = RelationToOne(name, model_name, converter)
    return converter


def Relation(path, converter):  # pylint: disable=invalid-name
    """Kept for compatibility but will be removed
    .. deprecated:: 1.2.0
       Use :func:`relation` instead, that uses PEP8 defined function case.
    """
    warnings.warn(
        "Deprecated function Relation, use relation instead",
        DeprecationWarning,
    )
    return relation(path, converter)

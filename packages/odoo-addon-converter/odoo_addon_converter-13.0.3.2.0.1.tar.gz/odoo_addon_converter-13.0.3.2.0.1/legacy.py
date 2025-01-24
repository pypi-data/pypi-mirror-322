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

"""
.. deprecated:: 1.0
  Use the other converter instead, kept for ease of porting.
"""

import warnings
from typing import Any, Dict, Optional

from odoo import api, models

from .base import Converter, Skip, logger
from .field import Field
from .model import Model
from .models.ir_model_data import _XREF_IMD_MODULE

warnings.warn("legacy converters are deprecated", DeprecationWarning)


class Many2oneConverter(Field):
    """Converts many2one xref."""

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        field_value = super().odoo_to_message(instance, ctx)
        if field_value is not Skip:
            return field_value.env["ir.model.data"].object_to_xmlid(
                field_value
            )
        if self.required_blank_value is not None:
            return self.required_blank_value
        return Skip

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
        # Empty string is considered as NULL
        rel_record_id = (
            odoo_env.ref(_XREF_IMD_MODULE, message_value).id
            if message_value
            else None
        )
        if instance:
            field_value = getattr(instance, self.field_name)
            if (
                rel_record_id and field_value.id == rel_record_id
            ) or not field_value:
                return {}
        return {self.field_name: rel_record_id}


class Many2manyConverter(Field):
    """Converts many2many xref."""

    def __init__(self, field_name: str, model_name: str):
        super().__init__(field_name)
        self.model_name = model_name

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        values = super().odoo_to_message(instance, ctx)
        return [
            value.env["ir.model.data"].object_to_xmlid(value)
            for value in values
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
            field_instances |= odoo_env["ir.model.data"].ref(
                _XREF_IMD_MODULE, value
            )
        if instance and getattr(instance, self.field_name) == field_instances:
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


class Many2oneFieldValueConverter(Field):
    """Converter for many2one field where a field of the many2one instance is
    used. The value must be unique by record.
    """

    def __init__(
        self,
        field_name: str,
        model_name: str,
        many2one_field_name: str = "name",
    ):
        super().__init__(field_name)
        self.model_name = model_name
        self.many2one_field_name = many2one_field_name

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        logger.debug(self.field_name)
        record = super().odoo_to_message(instance, ctx)
        if record is Skip:
            return Skip
        return getattr(record, self.many2one_field_name)

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
        field_instance = odoo_env[self.model_name].search(
            [(self.many2one_field_name, "=", message_value)]
        )
        if len(field_instance) > 1:
            logger.warning(
                "More than one match for %s: %s",
                self.many2one_field_name,
                field_instance,
            )
        if instance and getattr(instance, self.field_name) == field_instance:
            return {}
        return {self.field_name: field_instance.id}


class Many2manyFieldValueConverter(Field):
    """Converter for many2many field where a field of the many2one instance is
    used. The value must be unique by record.
    """

    def __init__(
        self,
        field_name: str,
        model_name: str,
        many2many_field_name: str = "name",
    ):
        super().__init__(field_name)
        self.model_name = model_name
        self.many2many_field_name = many2many_field_name

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        values = super().odoo_to_message(instance, ctx)
        if values is Skip:
            return Skip
        return [getattr(value, self.many2many_field_name) for value in values]

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
        field_instances = odoo_env[self.model_name].search(
            [(self.many2many_field_name, "in", message_value)]
        )
        if instance and getattr(instance, self.field_name) == field_instances:
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


class One2manyConverter(Model):
    def __init__(
        self,
        field_name: str,
        __type__: str,
        converters: Dict[str, Converter],
        model_name: str,
    ):
        super().__init__(__type__, converters)
        self.field_name = field_name
        self.model_name = model_name

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        return [
            msg
            for msg in (
                super().odoo_to_message(element, ctx)
                for element in getattr(instance, self.field_name)
            )
            if msg is not Skip
        ]

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.Model,
        value_present: bool = True,
    ) -> Dict:
        return {}

    def post_hook(self, instance: models.Model, message_data):
        if self.field_name in message_data:
            ids = []
            for element in message_data:
                o2m_instance = super().get_instance(instance.env, element)
                vals_by_context = super().message_to_odoo(
                    instance.env, "update", element, o2m_instance
                )
                if not o2m_instance:
                    context = dict(no_sync=True)
                    context_, vals = vals_by_context.popitem(last=False)
                    context.update(context_)
                    o2m_instance = (
                        instance.env[self.model_name]
                        .with_context(**context)
                        .create(vals)
                    )
                o2m_instance.context_write(vals_by_context)
                ids.append(o2m_instance.id)
                super().post_hook(o2m_instance, element)
            instance.with_context(no_sync=True).write(
                {self.field_name: [(6, 0, ids)]}
            )

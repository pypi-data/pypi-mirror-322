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

from typing import Any, Optional

from odoo import models

from .base import Converter


class KeyField(Converter):
    """Converter used when a field is used as a key.

    This is usually used with a RelationToX converter instead of a
    :class:Xref converter.

    The key must match only one model. Set limit_lookup to use the first model found.
    """

    def __init__(self, field_name: str, model_name: str, limit_lookup: bool = False):
        self.field_name = field_name
        self.model_name = model_name
        self.lookup_limit = 1 if limit_lookup else None

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[dict] = None
    ) -> Any:
        return getattr(instance, self.field_name)

    def get_instance(self, odoo_env, message_data):
        instance = odoo_env[self.model_name].search(
            [(self.field_name, "=", message_data)], limit=self.lookup_limit
        )
        if instance:
            instance.ensure_one()
        return instance

    @classmethod
    def is_instance_getter(cls) -> bool:
        return True

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

from typing import Any

from odoo import models

from .base import ContextBuilder, Converter, Skip, build_context


class List(Converter):
    """A converter that takes a list of converter"""

    def __init__(
        self,
        converters: list[Converter],
        context: ContextBuilder | None = None,
    ):
        super().__init__()
        self._converters = converters
        self.context = context

    def odoo_to_message(self, instance: models.Model, ctx: dict | None = None) -> Any:
        ctx = build_context(instance, ctx, self.context)

        message_data = []

        for converter in self._converters:
            value = converter.odoo_to_message(instance, ctx)
            if value is not Skip:
                message_data.append(value)

        return message_data

    def message_to_odoo(
        self,
        odoo_env,
        phase: str,
        message_value,
        instance: models.Model,
        value_present: bool = True,
    ) -> dict:
        return {}

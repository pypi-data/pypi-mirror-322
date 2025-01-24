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

import ast
from typing import Any, Dict, Optional

from odoo import models

from . import base


class MailTemplate(base.Converter):
    """This converter wraps ``mail.template::_render_template``.
    Multiple records are allowed but ``mail.template::render_template`` still
    runs once per record; to accomodate, we provide ``ctx["records"]``.
    """

    def __init__(self, template: str, post_eval: bool = False):
        self.template = template
        self.post_eval = post_eval

    def odoo_to_message(
        self, records: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        multiple_records = len(records) > 1
        record_ids_or_id = records.ids if multiple_records else records.id
        value = (
            records.env["mail.template"]
            .with_context(records=records, safe=True)
            ._render_template(self.template, records._name, record_ids_or_id)
        )
        if multiple_records:  # render_template outputs indexed by record ID
            value = value[records[0].id]
        if self.post_eval:
            value = ast.literal_eval(value)
        return value

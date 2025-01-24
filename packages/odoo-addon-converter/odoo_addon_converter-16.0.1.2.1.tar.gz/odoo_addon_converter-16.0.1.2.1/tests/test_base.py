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

from odoo import tests

from odoo.addons.converter import Constant, Field, Model, Xref, message_to_odoo


class Test(tests.TransactionCase):
    def setUp(self):
        super().setUp()
        self.active_user = self.env["res.users"].search(
            [("active", "=", True)], limit=1
        )

    def test_constant(self):
        converter = Constant("a")
        self.assertEqual("a", converter.odoo_to_message(self.env["res.users"]))

    def test_convert(self):
        converter = Model(
            None,
            {
                "active": Field("active"),
                "ref": Xref("base"),
                "name": Field("name"),
                "bic": Field("bic"),
            },
        )
        model_name = "res.bank"
        self.assertTrue(self.env.ref("base.bank_bnp").active)
        message_to_odoo(
            self.env,
            {"ref": "bank_bnp", "active": False},
            model_name,
            converter,
        )
        self.assertFalse(self.env.ref("base.bank_bnp").active)

        message_to_odoo(
            self.env,
            {
                "ref": "bank_new",
                "active": True,
                "name": "New Bank",
                "bic": "CBSBLT26",
            },
            model_name,
            converter,
        )

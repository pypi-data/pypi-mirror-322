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

import json
import os

import fastjsonschema

import odoo.addons

VALIDATION_SKIP = "skip"
VALIDATION_SOFT = "soft"
VALIDATION_STRICT = "strict"


class NotInitialized(Exception):
    pass


class Validator:
    def __init__(
        self,
        repository_module_name: str,
        repository: str,
        default_url_pattern: str,
    ):
        self.repository_module_name = repository_module_name
        self.repository = repository
        # exemple "https://annonces-legales.fr/xbus/schemas/v1/{}.schema.json"
        self.default_url_pattern = default_url_pattern
        self.validators = {}
        self.initialized = False
        self.encoding = "UTF-8"

    def initialize(self) -> None:
        repo_module_basepath = os.path.dirname(
            getattr(odoo.addons, self.repository_module_name).__file__
        )

        # Read local schema definitions.
        schemas = {}
        schema_search_path = os.path.abspath(
            os.path.join(repo_module_basepath, self.repository)
        )
        for root, _dirs, files in os.walk(schema_search_path):
            for fname in files:
                fpath = os.path.join(root, fname)
                if fpath.endswith((".json",)):
                    with open(fpath, "r", encoding=self.encoding) as schema_fd:
                        schema = json.load(schema_fd)
                        if "$id" in schema:
                            schemas[schema["$id"]] = schema

        # Prepare validators for each schema. We add an HTTPS handler that
        # points back to our schema definition cache built above.
        for schema_id, schema in schemas.items():
            self.validators[schema_id] = fastjsonschema.compile(
                schema,
                handlers={"https": lambda uri: schemas[uri]},
                use_default=False,
            )
        self.initialized = True

    def validate(self, schema_id, payload) -> None:
        if not self.initialized:
            raise NotInitialized("please call the initialize() method")

        self.validators[self.default_url_pattern.format(schema_id)](payload)

*******
History
*******

13.0.3.2.0
==========

Export constants from ``.base``.
Used by other modules; these exports got removed when I replaced an ``import *`` earlier.

``jsonschema`` ➔ ``fastjsonschema``.

13.0.3.1.0
==========

* Code formatting, add license / docs / badges.

(port from 11.0.1.2.0)

* MailTemplate converter: Allow multiple records.

3.0.2
=====

Fix issue with Switch and the use of Skip as a converter, also make switch send Skip when nothing matches its rules.

Fix issue with RelationToMany that always convert to Skip when send_empty is False.

Fix issue with chaining relation converter with empty values.

3.0.1
=====

Fix code errors.

3.0.0
=====

Change get__type__ to return a set of values.
It is defined at the Converter level despite only returning a value for a small number of Converters but it simplifies the code using it to do so that way.

Validation and validator can be set on converters after initialization. Only some converter makes use of those values.
This makes the message_to_odoo_validate method unnecessary, that’s why it has been removed.

2.0.0
=====

Change the Model converter to be able to use validators.

Add a legacy converter from orus_sync. It is deprecated and will be removed.

Add converter and ir_model tests from orus_sync.

Add the switch converter and fix it and its tests.

Include the functionnality of FirstKeyField in KeyField directly, marking it as deprecated.

1.2.1
=====

Fix relation reception, see ``tests/test_relation.py > test_many2one_to_odoo`` for a test case.

``get_instance`` functions can now return a ``Newinstance`` record (record being created).

1.2.0
=====

Add constant converter and a converter to use the translated values of a selection field.

Add tests, correct code so test passes.
Fix issues with some converter.

1.1.1
=====

Added CI configuration

1.1
===

* Field converter modified (to format the value if the field type is datetime)

1.0
===

Initial version.

Changelog
=========

15.0.3.3.2
----------

Fix RelationToMany calling undefined fonction.

15.0.3.3.1
----------

* In the converter of Many2one relations, the model name must be a keyword
  argument, optional and not compulsory, as in Odoo 11. Moreover, when the
  Many2one is empty and a value has to be returned, the converter tries to
  return the class of the Many2one model. The converter must be able to
  automatically identify the model name from the Many2one definition, without
  requiring the model name to be given in arguments.

15.0.3.3.0
----------

Make module installable.

15.0.3.2.0
----------

(port from 13.0.3.2.0)
~~~~~~~~~~~~~~~~~~~~~~

Export constants from ``.base``.
Used by other modules; these exports got removed when I replaced an ``import *`` earlier.

``jsonschema`` ➔ ``fastjsonschema``.

15.0.3.1.0
----------

(port from 13.0.3.1.0)
~~~~~~~~~~~~~~~~~~~~~~

* Code formatting, add license / docs / badges.

(port from 13.0.3.1.0 / 11.0.1.2.0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* MailTemplate converter: Allow multiple records.
* 15.0: In the process, also fix existing MailTemplate converter (found by these new tests).

(port from 13.0.3.0.2)
~~~~~~~~~~~~~~~~~~~~~~

Fix issue with Switch and the use of Skip as a converter, also make switch send Skip when nothing matches its rules.

Fix issue with RelationToMany that always convert to Skip when send_empty is False.

Fix issue with chaining relation converter with empty values.

15.0.3.0.0
----------

Update to use python 3.10 idioms.

15.0.2.0.0
----------

forward port of 13.0.3.0.0
~~~~~~~~~~~~~~~~~~~~~~~~~~

Change get__type__ to return a set of values.
It is defined at the Converter level despite only returning a value for a small number of Converters but it simplifies the code using it to do so that way.

Validation and validator can be set on converters after initialization. Only some converter makes use of those values.
This makes the message_to_odoo_validate method unnecessary, that’s why it has been removed.

15.0.1.0.0
----------

Migration to Odoo 15.0

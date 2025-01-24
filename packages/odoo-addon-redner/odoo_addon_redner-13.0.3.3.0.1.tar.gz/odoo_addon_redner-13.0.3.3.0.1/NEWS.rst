====
NEWS
====

13.0.3.3.0
==========

(port from 11.0.2.8.0)

* Server URL rework: Expect an URL without path, add /api/v1 in the code.

13.0.3.2.0
==========

(forward port of 11.0.2.7.0)

Improve search view of redner templates.

13.0.3.1.1
==========

Fix import of relation from converter module.

13.0.3.1.0
==========

(forward port of 11.0.2.6.0)

Redner server an use an unix socket too so also handle it.


(forward port of 11.0.2.5.0)

* Configurable timeout for redner calls, default is 20 seconds.

13.0.3.0.2
==========

Fix a docstring (not an override).
Credit OCA for report code.
Improve logging - request contents only logged at debug level.
Move redner.py outside of the models directory.

13.0.3.0.1
==========

Save template redner as an attachment

13.0.3.0.0
==========

Move constant converter to converter module.

13.0.2.0.1
==========

Bug Fixes

    * fix (ir.actions.report): Defines missing `get_from_report_name` method.
    * fix (__manifest__): Add missing dependency to `converter`.


13.0.2.0.0
==========

* Migrate to Odoo 13.0.
* Add a new template engine "od+mustache"

11.0.2.2
========

* Previous working 11.0 version.

=========
Changelog
=========

16.0.1.3.0
----------

Extend mail compose functionality to support Redner templates in mass mailing.

16.0.1.2.3
----------

Refactor function name and update references.

16.0.1.2.2
----------

Return original expression for non-matching regex in `parse_sorted_field`.

16.0.1.2.1
----------

Update version number in manifest.

16.0.1.2.0
----------

FIX redner optional report error.

Introduces sorting capabilities within the Redner substitution.

16.0.1.1.2
----------

Move the ``detected_keywords`` field to a dedicated  ``Variables`` tab.

16.0.1.1.1
----------

Loosen up python version.

16.0.1.1.0
----------

Use pypdf (3+) if present, otherwise defaults to PyPDF2.

16.0.1.0.3
----------

Put back default template value.

16.0.1.0.2
----------

Fix missing default language when creating from another model’s form.

16.0.1.0.1
----------

* Fix display of model rendering variables.

16.0.1.0.0
----------

* Migrate to Odoo 16.0.

15.0.1.0.0
----------

* Migrate to Odoo 15.0.

13.0.3.4.0
----------

(port from 11.0.2.9.0)

* Code formatting, add license / docs / badges.
* Add tests.
* Update various labels.
* Update French translations.

(port from 11.0.2.8.1)

* Fix send_to_rednerd_server to handle ODT document.

(port from 11.0.2.5.1)

* Sort substitutions by keyword to improve readability in redner report.
* Add confirmation on the get substitutions button to protect it from unwanted actions.

(port from 11.0.2.4.0)

* Allow 1 report on multiple records.

(port from 11.0)

* Include touch-ups/evolutions done during 13.0➔11.0 converter backport in 2021-06.
  In particular, add "HTML + mustache" / "MJML + mustache" instead of just "mustache".

13.0.3.3.0
----------

(port from 11.0.2.8.0)

* Server URL rework: Expect an URL without path, add /api/v1 in the code.

13.0.3.2.0
----------

(forward port of 11.0.2.7.0)

Improve search view of redner templates.

13.0.3.1.1
----------

Fix import of relation from converter module.

13.0.3.1.0
----------

(forward port of 11.0.2.6.0)

Redner server an use an unix socket too so also handle it.

(forward port of 11.0.2.5.0)

* Configurable timeout for redner calls, default is 20 seconds.

13.0.3.0.2
----------

* Fix a docstring (not an override).
* Credit OCA for report code.
* Improve logging - request contents only logged at debug level.
* Move redner.py outside of the models directory.

13.0.3.0.1
----------

Save template redner as an attachment

13.0.3.0.0
----------

Move constant converter to converter module.

13.0.2.0.1
----------

Bug Fixes:

* fix (ir.actions.report): Defines missing ``get_from_report_name`` method.
* fix (__manifest__): Add missing dependency to ``converter``.

13.0.2.0.0
----------

* Migrate to Odoo 13.0.
* Add a new template engine "od+mustache"

11.0.2.2
--------

* Previous working 11.0 version.

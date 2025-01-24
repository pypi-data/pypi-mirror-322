======
Redner
======

Redner is an innovative solution to produce transactional emails
and documents in PDF or HTML format.

It's designed to help applications or websites that need to send transactional
email like password resets, order confirmations, and welcome messages.

Redner offers advanced tracking, easy-to-understand reports & email
templates.
This Module allow you to use email template designed with mailjet app
(languages uses in template must be mjml or mustache) which you can add
in odoo template.
It also allows the rendering of documents in pdf or html format.

Configure this module using the following ``ir.config_parameter``::

    redner.server_url = http://dockerhost:7000
    redner.api_key = <your API key here>
    redner.account = <your account name>
    redner.timeout = 20

``redner.timeout`` is in seconds; defaults to 20 seconds per redner call.

**Pro tip**: You can use mjml-app_ to prototype your email templates.

UI Changes
----------

* Setting > Redner > Templates

Note: When you have existing templates you want to register onto a new
redner server (or with a new user), multi-select them and click
"Send to redner server".

.. _mjml-app: http://mjmlio.github.io/mjml-app/

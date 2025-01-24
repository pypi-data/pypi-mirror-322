##############################################################################
#
#    Redner Odoo module
#    Copyright © 2016 XCG Consulting <https://xcg-consulting.fr>
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

import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ..redner import Redner

logger = logging.getLogger(__name__)

_redner = None


class RednerTemplate(models.Model):
    _name = "redner.template"
    _description = "Redner Template"

    name = fields.Char(
        string="Name",
        required=True,
        help="This is a name of template mjml redner",
    )

    body = fields.Text(
        string="Template remote Id",
        translate=True,
        help="Code for the mjml redner template must be added here",
    )

    slug = fields.Char(string="Slug")

    active = fields.Boolean(
        string="Active",
        default=True,
        help=(
            "If unchecked, it will allow you to hide the "
            "template without removing it."
        ),
    )

    is_mjml = fields.Boolean(
        string="Is MJML",
        default=True,
        help="set to false if your template doesn't contain MJML",
    )

    detected_keywords = fields.Text(
        string="Variables", readonly=True, compute="_compute_keywords"
    )

    language = fields.Selection(
        string="Language",
        selection=[
            ("text/html|mustache", "HTML + mustache"),
            ("text/mjml|mustache", "MJML + mustache"),
            (
                "application/vnd.oasis.opendocument.text|od+mustache",
                "OpenDocument + mustache",
            ),
        ],
        default="text/html|mustache",
        required=True,
        help="templating language",
    )

    redner_id = fields.Char(string="Redner ID", readonly=True)

    locale_id = fields.Many2one(
        comodel_name="res.lang",
        string="Locale",
        help="Optional translation language (ISO code).",
    )

    template_data = fields.Binary("Libreoffice Template")

    @property
    def redner(self):
        """Try to avoid Redner instance to be over created"""
        global _redner
        if _redner is None:
            # Bypass security rules when reading these configuration params. By
            # default, only some administrators have access to that model.
            config_model = self.env["ir.config_parameter"].sudo()

            _redner = Redner(
                config_model.get_param("redner.api_key"),
                config_model.get_param("redner.server_url"),
                config_model.get_param("redner.account"),
                int(config_model.get_param("redner.timeout", default="20")),
            )

        return _redner

    @api.model
    def create(self, vals):
        """Overwrite create to create redner template"""

        # Prepare template params according to the selected language.
        # Use template data field if the selected language is "od";
        # otherwise the body field is used.
        produces, language = vals.get("language").split("|")
        body, body_format = (
            (vals.get("template_data", ""), "base64")
            if language == "od+mustache"
            else (vals.get("body"), "text")
        )

        # We depend on the API for consistency here
        # So raised error should not result with a created template
        vals["redner_id"] = self.redner.templates.account_template_add(
            language=language,
            body=body,
            name=vals.get("name"),
            produces=produces,
            body_format=body_format,
            version=fields.Datetime.to_string(fields.Datetime.now()),
        )

        return super().create(vals)

    def write(self, vals):
        """Overwrite write to update redner template"""

        # Similar to the "send_to_rednerd_server" method; not worth factoring
        # out.

        # We depend on the API for consistency here
        # So raised error should not result with an updated template
        if "name" in vals:
            self.ensure_one()

            redner_id = self.redner_id
            vals["redner_id"] = vals["name"]

        ret = super().write(vals)
        for record in self:
            try:
                produces, language = record.language.split("|")
                body, body_format = (
                    (record.template_data.decode(), "base64")
                    if language == "od+mustache"
                    else (record.body, "text")
                )

                if "name" not in vals:
                    redner_id = record.redner_id

                record.redner.templates.account_template_update(
                    template_id=redner_id,
                    language=language,
                    body=body,
                    name=vals.get("name", ""),
                    produces=produces,
                    body_format=body_format,
                    version=fields.Datetime.to_string(record.write_date),
                )
            except Exception as e:
                logger.error("Failed to update redner template :%s", e)
                raise ValidationError(
                    _("Failed to update render template, %s") % e
                ) from e
        return ret

    def unlink(self):
        """Overwrite unlink to delete redner template"""

        # We do NOT depend on the API for consistency here
        # So raised error should not result block template deletion
        try:
            self.redner.templates.account_template_delete(self.redner_id)
        except Exception:
            pass

        return super().unlink()

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, name=_("%s (copy)") % self.name)
        return super().copy(default)

    @api.depends("body", "template_data")
    def _compute_keywords(self):
        for record in self:
            record.detected_keywords = record.template_varlist_fetch()

    @api.model
    def get_keywords(self):
        """Return template redner keywords"""

        varlist = self.template_varlist_fetch()

        for name in varlist:
            while "." in name:
                name = name[: name.rfind(".")]
                if name not in varlist:
                    varlist.append(name)

        varlist.sort()

        return varlist

    @api.model
    def template_varlist_fetch(self):
        """Retrieve the list of variables present in the template."""
        try:
            if not self.redner_id:
                return []

            return self.redner.templates.account_template_varlist(self.redner_id)

        except Exception as e:
            logger.warning("Failed to fetch account template varlist: %s" % e)
            return []

    def send_to_rednerd_server(self):
        """Send templates to the rednerd server. Useful when you have
        existing templates you want to register onto a new rednerd server (or
        with a new user).
        """
        for record in self:
            # Similar to the "write" method override; not worth factoring out.
            templates = record.redner.templates

            produces, language = record.language.split("|")

            body, body_format = (
                (record.template_data.decode(), "base64")
                if language == "od+mustache"
                else (record.body, "text")
            )

            try:
                templates.account_template_update(
                    template_id=record.redner_id,
                    language=language,
                    body=body,
                    name=record.name,
                    produces=produces,
                    body_format=body_format,
                    version=fields.Datetime.to_string(record.write_date),
                )
            except ValidationError:
                record.redner_id = templates.account_template_add(
                    language=language,
                    body=body,
                    name=record.name,
                    produces=produces,
                    body_format=body_format,
                    version=fields.Datetime.to_string(fields.Datetime.now()),
                )

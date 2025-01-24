import base64
import logging

from odoo import _, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)


def image(value):
    # get MIME type associated with the decoded_data.
    image_base64 = base64.b64decode(value)
    mimetype = guess_mimetype(image_base64)
    return {"body": value.decode("utf-8"), "mime-type": mimetype}


class MailTemplate(models.Model):
    """Extended to add features of redner API"""

    _inherit = "mail.template"

    is_redner_template = fields.Boolean(
        string="Is redner template?",
        default=False,
        help="Check this box if this template is a redner. "
        "If it's not checked, it assumes that the default "
        "email template odoo to be used.",
    )

    redner_tmpl_id = fields.Many2one(
        comodel_name="redner.template",
        string="Redner Template",
        domain=[("active", "=", True)],
    )

    redner_substitution_ids = fields.One2many(
        comodel_name="redner.substitution",
        inverse_name="template_id",
        string="Substitutions",
    )

    def action_get_substitutions(self):
        """Call by: action button `Get Substitutions from Redner Template`"""
        self.ensure_one()

        if self.redner_tmpl_id:
            keywords = self.redner_tmpl_id.get_keywords()

            # Get current substitutions
            subs = self.redner_substitution_ids.mapped("keyword") or []
            values = []
            for key in keywords:
                # check to avoid duplicate keys
                if key not in subs:
                    values.append((0, 0, {"keyword": key}))
            self.write({"redner_substitution_ids": values})

            # remove obsolete keywords in substitutions model
            if len(self.redner_substitution_ids) > len(keywords):
                deprecated_keys = self.redner_substitution_ids.filtered(
                    lambda s: s.keyword not in keywords
                )
                if len(deprecated_keys) > 0:
                    deprecated_keys.unlink()

    def _patch_email_values(self, values, res_id):

        conv = self.redner_substitution_ids.filtered(
            lambda r: r.depth == 0
        ).build_converter()

        instance = self.env[self.model].browse(res_id)

        values_sent_to_redner = conv.odoo_to_message(instance)

        try:
            res = self.redner_tmpl_id.redner.templates.render(
                self.redner_tmpl_id.redner_id, values_sent_to_redner
            )
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(
                _(
                    "We received an unexpected error from redner server. "
                    "Please contact your administrator"
                )
            ) from e
        values["body_html"] = (
            base64.b64decode(res[0]["body"]).decode("utf-8") if res else ""
        )
        values["body"] = values["body_html"]

        return values

    def generate_email(self, res_ids, fields=None):
        self.ensure_one()

        results = super().generate_email(res_ids, fields=fields)
        if not self.is_redner_template:
            return results

        multi_mode = True
        if isinstance(res_ids, int):
            res_ids = [res_ids]
            multi_mode = False

        if multi_mode:
            return {
                res_id: self._patch_email_values(values, res_id)
                for res_id, values in results.items()
            }
        return self._patch_email_values(results, res_ids[0])

    def render_variable_hook(self, variables):
        """Override to add additional variables in mail "render template" func
        """
        variables.update({"image": image})
        return super().render_variable_hook(variables)

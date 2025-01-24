import base64
import logging
import time

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval

from ..utils.formats import Formats

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    """
    Inherit from ir.action.report to allow customizing the template
    file.
    """

    _inherit = "ir.actions.report"

    @api.constrains("redner_filetype", "report_type")
    def _check_redner_filetype(self):
        for report in self:
            if report.report_type == "redner" and not report.redner_filetype:
                raise ValidationError(
                    _("Field 'Output Format' is required for Redner report")
                )

    @api.constrains("redner_filetype", "attachment")
    def _check_redner_attachment(self):
        for report in self:
            if report.report_type == "redner" and report.attachment:
                ext = ".{ftype}".format(ftype=report.redner_filetype)
                if ext not in report.attachment:
                    raise ValidationError(
                        _(
                            "The output format cannot be different from the "
                            'extension defined in "Save as attachment prefix".'
                        )
                    )

    @api.model
    def _get_redner_filetypes(self):
        formats = Formats()
        names = formats.get_known_format_names()
        selections = []
        for name in names:
            description = name
            if formats.get_format(name).native:
                description = description + " " + _("(Native)")
            selections.append((name, description))
        return selections

    report_type = fields.Selection(selection_add=[("redner", "redner")])

    redner_multi_in_one = fields.Boolean(
        string="Multiple Records in a Single Redner Report",
        help="If you execute a report on several records, "
        "by default Odoo will generate a ZIP file that contains as many "
        "files as selected records. If you enable this option, Odoo will "
        "generate instead a single report for the selected records.",
    )

    redner_filetype = fields.Selection(
        selection="_get_redner_filetypes", string="Redner Output Format"
    )

    is_redner_native_format = fields.Boolean(
        compute="_compute_is_redner_native_format"
    )

    redner_tmpl_id = fields.Many2one(
        comodel_name="redner.template",
        string="Redner template",
        domain=[("active", "=", True)],
    )

    substitution_ids = fields.One2many(
        comodel_name="redner.substitution",
        inverse_name="ir_actions_report_id",
        string="Substitution",
    )

    @api.depends("report_type", "redner_filetype")
    def _compute_is_redner_native_format(self):
        fmt = Formats()
        for rec in self:
            rec.is_redner_native_format = False
            if not rec.report_type == "redner" or not rec.redner_filetype:
                continue
            filetype = rec.redner_filetype
            rec.is_redner_native_format = fmt.get_format(filetype).native

    def action_get_substitutions(self):
        """Call by: action button `Get Substitutions from Redner Report`"""
        self.ensure_one()

        if self.redner_tmpl_id:
            keywords = self.redner_tmpl_id.get_keywords()

            # Get current substitutions
            subs = self.substitution_ids.mapped("keyword") or []
            values = []
            for key in keywords:
                # check to avoid duplicate keys
                if key not in subs:
                    values.append((0, 0, {"keyword": key}))
            self.write({"substitution_ids": values})

            # remove obsolete keywords in substitutions model
            if len(self.substitution_ids) > len(keywords):
                deprecated_keys = self.substitution_ids.filtered(
                    lambda s: s.keyword not in keywords
                )
                if len(deprecated_keys) > 0:
                    deprecated_keys.unlink()

    def get_report_metadata(self):
        self.ensure_one()

        metadata_values = {}

        pformat = self.paperformat_id
        if not pformat:
            return metadata_values

        # Get print-paper-size values
        if pformat.format and pformat.orientation:
            metadata_values["print-paper-size"] = "%s %s" % (
                pformat.format,
                pformat.orientation,
            )
        elif pformat.format and not pformat.orientation:
            metadata_values["print-paper-size"] = "%s" % pformat.format

        # Get print-paper-margin values: top | right | bottom | left
        metadata_values["print-paper-margin"] = "%s %s %s %s" % (
            pformat.margin_top,
            pformat.margin_right,
            pformat.margin_bottom,
            pformat.margin_left,
        )

        return metadata_values

    def get_report_data(self, res_id):
        if not res_id:
            return {}

        conv = self.substitution_ids.filtered(
            lambda r: r.depth == 0
        ).build_converter()

        instance = self.env[self.model].browse(res_id)

        return conv.odoo_to_message(instance)

    @api.model
    def get_from_report_name(self, report_name, report_type):
        return self.search(
            [
                ("report_name", "=", report_name),
                ("report_type", "=", report_type),
            ]
        )

    def render_redner(self, res_ids, data):
        self.ensure_one()
        if self.report_type != "redner":
            raise RuntimeError(
                "redner rendition is only available on redner report.\n"
                "(current: '{}', expected 'redner'".format(self.report_type)
            )
        return (
            self.env["redner.report"]
            .create({"ir_actions_report_id": self.id})
            .create_report(res_ids, data)
        )

    def gen_report_download_filename(self, res_ids, data):
        """Override this function to change the name of the downloaded
        report"""

        self.ensure_one()
        report = self.get_from_report_name(self.report_name, self.report_type)
        if report.print_report_name and not len(res_ids) > 1:
            obj = self.env[self.model].browse(res_ids)
            return safe_eval(
                report.print_report_name, {"object": obj, "time": time}
            )
        return "{}.{}".format(self.name, self.redner_filetype)

    def _get_attachments(self, res_ids):
        """Return the report already generated for the given res_ids"""
        self.ensure_one()
        save_in_attachment = {}
        if res_ids:
            # Dispatch the records by ones having an attachment
            model = self.env[self.model]
            record_ids = model.browse(res_ids)
            if self.attachment:
                for record_id in record_ids:
                    attachment_id = self.retrieve_attachment(record_id)
                    if attachment_id:
                        save_in_attachment[record_id.id] = attachment_id
        return save_in_attachment

    def postprocess_redner_report(self, record, buffer):
        """Handle post processing during the report generation.
        The basic behavior consists to create a new attachment containing
        the document base64 encoded.
        """

        self.ensure_one()

        attachment_name = safe_eval(
            self.attachment, {"object": record, "time": time}
        )

        if not attachment_name:
            return None

        if not attachment_name.endswith(
            ".{filetype}".format(filetype=self.redner_filetype)
        ):
            return None

        attachment_vals = {
            "name": attachment_name,
            "datas": base64.encodestring(buffer.getvalue()),
            "res_model": self.model,
            "res_id": record.id,
            "type": "binary",
        }
        try:
            self.env["ir.attachment"].create(attachment_vals)
        except AccessError:
            _logger.info(
                "Cannot save report %r as attachment", attachment_vals["name"]
            )
        else:
            _logger.info(
                "The document %s is now saved in the database",
                attachment_vals["name"],
            )
        return buffer

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons import converter

from ..converter import ImageDataURL, ImageFile


class Substitution(models.Model):
    """Substitution values for a Redner email message"""

    _name = "redner.substitution"

    _description = "Redner Substitution"

    keyword = fields.Char(string="Variable", help="Template variable name")

    template_id = fields.Many2one(
        comodel_name="mail.template", string="Use template"
    )

    ir_actions_report_id = fields.Many2one(
        comodel_name="ir.actions.report", string="Use report"
    )

    value = fields.Char(string="Expression")

    converter = fields.Selection(
        selection=[
            ("mail_template", "Odoo Template"),
            ("mail_template+deserialize", "Odoo Template + Eval"),
            ("field", "Field"),
            ("image-file", "Image file"),
            ("image-data-url", "Image data url"),
            ("relation-to-many", "Relation to many"),
            ("relation-path", "Relation Path"),
            ("constant", "Constant value"),
        ]
    )

    depth = fields.Integer(
        string="Depth", compute="_compute_depth", store=True
    )

    @api.depends("keyword")
    def _compute_depth(self):
        for record in self:
            record.depth = record.keyword.count(".")

    def get_children(self):
        return self.search(
            [
                ("ir_actions_report_id", "=", self.ir_actions_report_id.id),
                ("keyword", "=like", self.keyword + ".%"),
                ("depth", "=", self.depth + 1),
            ]
        )

    def build_converter(self):
        d = {}
        for sub in self:
            if sub.converter == "mail_template":
                conv = converter.MailTemplate(sub.value, False)
            elif sub.converter == "mail_template+deserialize":
                conv = converter.MailTemplate(sub.value, True)
            elif sub.converter == "constant":
                conv = converter.Constant(sub.value)
            elif sub.converter == "field":
                if "." in sub.value:
                    path, name = sub.value.rsplit(".", 1)
                else:
                    path, name = None, sub.value
                conv = converter.Field(name)
                if path:
                    conv = converter.relation(path.replace(".", "/"), conv)
            elif sub.converter == "image-file":
                conv = ImageFile(sub.value)
            elif sub.converter == "image-data-url":
                conv = ImageDataURL(sub.value)
            elif sub.converter == "relation-to-many":
                conv = converter.RelationToMany(
                    sub.value,
                    None,
                    converter=sub.get_children().build_converter(),
                )
            elif sub.converter == "relation-path":
                conv = converter.relation(
                    sub.value, sub.get_children().build_converter()
                )
            elif sub.converter is False:
                continue
            else:
                raise ValidationError(
                    _("invalid converter type: %s") % sub.converter
                )
            d[sub.keyword.rsplit(".", 2)[-1]] = conv

        return converter.Model("", d)

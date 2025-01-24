import base64
from typing import Any, Dict, Optional

from odoo import models
from odoo.tools.mimetypes import guess_mimetype

from odoo.addons.converter import Converter


class ImageFile(Converter):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return {}

        content = base64.b64decode(value)
        mimetype = guess_mimetype(content)

        return {"body": value.decode("ascii"), "mime-type": mimetype}


class ImageDataURL(Converter):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def odoo_to_message(
        self, instance: models.Model, ctx: Optional[Dict] = None
    ) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return {}

        content = base64.b64decode(value)
        mimetype = guess_mimetype(content)

        return "data:%s;base64,%s" % (mimetype, value.decode("ascii"))

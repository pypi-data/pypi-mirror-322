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

import base64
from typing import Any

from odoo import models
from odoo.addons.converter import Converter
from odoo.tools.mimetypes import guess_mimetype


class ImageFile(Converter):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def odoo_to_message(self, instance: models.Model, ctx: dict | None = None) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return {}

        content = base64.b64decode(value)
        mimetype = guess_mimetype(content)

        return {"body": value.decode("ascii"), "mime-type": mimetype}


class ImageDataURL(Converter):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def odoo_to_message(self, instance: models.Model, ctx: dict | None = None) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return ""

        content = base64.b64decode(value)
        mimetype = guess_mimetype(content)

        return "data:{};base64,{}".format(mimetype, value.decode("ascii"))

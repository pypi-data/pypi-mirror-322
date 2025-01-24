###############################################################################
#
#    Redner Odoo module
#    Copyright © 2016, 2022 XCG Consulting (https://www.xcg-consulting.fr/)
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
###############################################################################
{
    "name": "Redner",
    "license": "AGPL-3",
    "summary": """
Allows to generate transactional emails and documents in PDF or HTML format""",
    "version": "13.0.3.3.0",
    "category": "Technical",
    "author": "XCG Consulting",
    "website": "https://www.xcg-consulting.fr/",
    "depends": ["base", "mail", "converter"],
    "data": [
        "security/ir.model.access.csv",
        "views/redner_template_views.xml",
        "views/mail_template_views.xml",
        "views/ir_actions_report.xml",
        "views/report_redner.xml",
        "views/menu.xml",
    ],
    "external_dependencies": {"python": ["requests_unixsocket"]},
    "demo": [],
}

##############################################################################
#
#    Redner Odoo module
#    Copyright © 2023 XCG Consulting <https://xcg-consulting.fr>
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

from unittest import mock

from odoo import fields

from .common import TestCommon

TEMPLATE_URL = "https://test-redner-url/api/v1/template/test-account"


class Test(TestCommon):
    """Test redner template management & their HTTP calls."""

    @mock.patch("requests.sessions.Session.put")
    @mock.patch("requests.sessions.Session.post")
    def test_http_calls(self, requests_post_mock, requests_put_mock):
        """Test HTTP calls while managing redner templates from Odoo."""

        # Our mocks return success codes.
        success_mock = mock.Mock(
            status_code=200, json=lambda: {"name": "test-redner-id"}
        )
        requests_post_mock.return_value = success_mock
        requests_put_mock.return_value = success_mock

        # Create a template. Default "language" value needed, see ::create.
        values = self.env["redner.template"].default_get(["language"])
        values.update({"name": "test-name", "body": "test-body"})
        redner_template = self.env["redner.template"].create(values)
        self.assertEqual(redner_template.redner_id, "test-redner-id")
        requests_put_mock.assert_not_called()
        requests_post_mock.assert_called_once_with(
            TEMPLATE_URL,
            json={
                "name": "test-name",
                "language": "mustache",
                "body": "test-body",
                "produces": "text/html",
                "body-format": "text",
                "locale": "fr_FR",
                "version": fields.Datetime.to_string(redner_template.create_date),
            },
            headers={"Rednerd-API-Key": "test-api-key"},
            timeout=20,
        )
        requests_post_mock.reset_mock()

        # Update template.
        redner_template.name = "test-name-2"
        requests_post_mock.assert_not_called()
        requests_put_mock.assert_called_once_with(
            TEMPLATE_URL + "/test-redner-id",
            json={
                "name": "test-name-2",
                "language": "mustache",
                "body": "test-body",
                "produces": "text/html",
                "body-format": "text",
                "locale": "fr_FR",
                "version": fields.Datetime.to_string(redner_template.write_date),
            },
            headers={"Rednerd-API-Key": "test-api-key"},
            timeout=20,
        )
        requests_put_mock.reset_mock()

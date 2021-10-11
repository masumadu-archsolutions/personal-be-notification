from tests.base_test_case import BaseTestCase
from unittest import mock


class TestSmsController(BaseTestCase):
    @mock.patch("app.controllers.sms_controller.send_sms")
    def test_send_message(self, mock_send_sms):
        sms_template = self.template

        sms_details = {"username": "john"}

        meta = {"type": sms_template.type, "subtype": sms_template.subtype}

        recipient = "0241112223"

        self.sms_controller.send_message(
            {"recipient": recipient, "details": sms_details, "meta": meta}
        )
        mock_send_sms.delay.assert_called()

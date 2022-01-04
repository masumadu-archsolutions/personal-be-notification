from tests.base_test_case import BaseTestCase

# from unittest import mock
# from app.tasks.sms_task import send_sms


class TestSmsController(BaseTestCase):
    pass
    # @mock.patch("app.controllers.tasks")
    # def test_send_message(self):
    #     sms_template = self.template
    #
    #     sms_details = {"username": "john"}
    #
    #     meta = {"type": sms_template.type, "subtype": sms_template.subtype}
    #
    #     recipient = "0241112223"
    #     with mock.patch.object(send_sms, "delay") as mock_send_sms:
    #         self.sms_controller.send_message(
    #             {"recipient": recipient, "details": sms_details, "meta": meta}
    #         )
    #     self.assertTrue(mock_send_sms.called)

from unittest import mock

import pytest

from app.core.exceptions import AppException
from app.core.result import Result
from app.models import NotificationTemplateModel, SMSModel
from tests import BaseTestCase


class TestSmsController(BaseTestCase):
    @pytest.mark.controller
    def test_index(self):
        self.assertEqual(SMSModel.query.count(), 1)
        get_all_sms = self.sms_controller.index()
        self.assertIsInstance(get_all_sms, Result)
        self.assertEqual(get_all_sms.status_code, 200)
        self.assertIsInstance(get_all_sms.value, list)

    @pytest.mark.controller
    def test_show(self):
        self.assertEqual(SMSModel.query.count(), 1)
        get_sms = self.sms_controller.show(self.sms_model.id)
        self.assertIsNotNone(get_sms)
        self.assertIsInstance(get_sms, Result)
        self.assertEqual(get_sms.status_code, 200)
        self.assertIsInstance(get_sms.value, SMSModel)
        self.assertEqual(get_sms.value, self.sms_model)

    @pytest.mark.controller
    @mock.patch("app.init_celery")
    def test_send_message(self, mock_celery):
        mock_celery.side_effect = self.init_celery
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        self.assertEqual(SMSModel.query.count(), 1)
        with mock.patch("app.tasks.sms_task.send_sms.delay") as mock_delay:
            self.sms_controller.send_message(self.sms_test_data.new_sms)
        self.assertTrue(mock_delay.called)
        exception_data = self.sms_test_data.new_sms
        exception_data["meta"]["subtype"] = "pin_change"
        template_error = self.sms_test_data.new_sms
        template_error["meta"]["subtype"] = "pin_change"
        self.assertIsNone(self.sms_controller.send_message(template_error))

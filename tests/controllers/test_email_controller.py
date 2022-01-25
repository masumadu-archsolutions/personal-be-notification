from unittest import mock

import pytest

from app.core.result import Result
from app.models import EmailModel, NotificationTemplateModel
from tests import BaseTestCase


class TestEmailController(BaseTestCase):
    @pytest.mark.controller
    def test_index(self):
        self.assertEqual(EmailModel.query.count(), 1)
        get_all_email = self.sms_controller.index()
        self.assertIsInstance(get_all_email, Result)
        self.assertEqual(get_all_email.status_code, 200)
        self.assertIsInstance(get_all_email.value, list)

    @pytest.mark.controller
    def test_show(self):
        self.assertEqual(EmailModel.query.count(), 1)
        get_email = self.email_controller.show(self.email_model.id)
        self.assertIsNotNone(get_email)
        self.assertIsInstance(get_email, Result)
        self.assertEqual(get_email.status_code, 200)
        self.assertIsInstance(get_email.value, EmailModel)
        self.assertEqual(get_email.value, self.email_model)

    @pytest.mark.controller
    @mock.patch("app.init_celery")
    def test_send_email(self, mock_celery):
        mock_celery.side_effect = self.init_celery
        self.assertEqual(NotificationTemplateModel.query.count(), 2)
        self.assertEqual(EmailModel.query.count(), 1)
        with mock.patch("app.tasks.email_task.send_email.delay") as mock_delay:
            self.email_controller.send_mail(self.email_test_data.new_email)
        self.assertTrue(mock_delay.called)
        template_error = self.email_test_data.new_email
        template_error["meta"]["subtype"] = "pin_change"
        self.assertIsNone(self.email_controller.send_mail(template_error))

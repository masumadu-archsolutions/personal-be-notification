from unittest import mock

import pytest

from tests import BaseTestCase


class TestEMailService(BaseTestCase):
    @pytest.mark.controller
    @mock.patch("app.services.email_service.SendGridAPIClient.send")
    def test_send_email(self, mock_sendgrid):
        email_record = self.email_test_data.send_email
        email_record["email_id"] = self.email_model.id
        mock_sendgrid.side_effect = self.side_effect.send_email_response
        with mock.patch("app.init_celery", side_effect=self.init_celery):
            from app.tasks import send_email

            send_email(
                email_record,
                self.email_service.__class__.__name__,
                self.email_repository.__class__.__name__,
            )

    @pytest.mark.controller
    @mock.patch("app.services.email_service.SendGridAPIClient.send")
    def test_send_email_exc(self, mock_sendgrid):
        email_record = self.email_test_data.send_email
        email_record["email_id"] = self.email_model.id
        mock_sendgrid.side_effect = self.side_effect.sendgrid_exception
        with mock.patch("app.init_celery", side_effect=self.init_celery):
            from app.tasks import send_email

            send_email(
                email_record,
                self.email_service.__class__.__name__,
                self.email_repository.__class__.__name__,
            )

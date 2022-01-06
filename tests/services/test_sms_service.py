from unittest import mock

import pytest

from tests import BaseTestCase


class TestSMSService(BaseTestCase):
    @pytest.mark.controller
    @mock.patch("app.services.sms_service.request")
    def test_send_sms(self, mock_requests):
        sms_record = self.sms_test_data.send_sms
        sms_record["message_id"] = self.sms_model.id
        mock_requests.side_effect = self.side_effect.send_sms_response
        with mock.patch("app.init_celery", side_effect=self.init_celery):
            from app.tasks import send_sms

            send_sms(
                sms_record,
                self.sms_service.__class__.__name__,
                self.sms_repository.__class__.__name__,
            )

    @pytest.mark.controller
    @mock.patch("app.services.sms_service.request")
    def test_send_sms_exc(self, mock_requests):
        sms_record = self.sms_test_data.send_sms
        sms_record["message_id"] = self.sms_model.id
        mock_requests.side_effect = self.side_effect.request_exception
        with mock.patch("app.init_celery", side_effect=self.init_celery):
            from app.tasks import send_sms

            send_sms(
                sms_record,
                self.sms_service.__class__.__name__,
                self.sms_repository.__class__.__name__,
            )

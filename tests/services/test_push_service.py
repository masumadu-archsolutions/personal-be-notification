from unittest import mock

import pytest

from tests import BaseTestCase


class TestPushNotificationService(BaseTestCase):
    @pytest.mark.controller
    @mock.patch("app.services.push_service.webpush")
    def test_send_push(self, mock_webpush):
        mock_webpush.side_effect = self.side_effect.send_push_response
        push_data = self.push_subscription_test_data.send_push
        push_data["endpoint_id"] = self.push_subscription_model.id
        with mock.patch("app.init_celery", side_effect=self.init_celery):
            from app.tasks import send_push

            send_push(
                push_data,
                self.push_service.__class__.__name__,
                self.push_subscription_repository.__class__.__name__,
            )

    @pytest.mark.controller
    @mock.patch("app.services.push_service.webpush")
    def test_send_push_exc(self, mock_webpush):
        push_data = self.push_subscription_test_data.send_push
        push_data["endpoint_id"] = self.push_subscription_model.id
        mock_webpush.side_effect = self.side_effect.pywebpush_exception
        with mock.patch("app.init_celery", side_effect=self.init_celery):
            from app.tasks import send_push

            send_push(
                push_data,
                self.push_service.__class__.__name__,
                self.push_subscription_repository.__class__.__name__,
            )

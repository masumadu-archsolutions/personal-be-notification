import pytest

from app.models import PushMessageModel, PushSubscriptionModel
from tests import BaseTestCase


class TestPushNotificationModels(BaseTestCase):
    @pytest.mark.model
    def test_push_message_model(self):
        self.assertEqual(PushMessageModel.query.count(), 1)
        result = PushMessageModel.query.get(self.push_message_model.id)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "message_type"))
        self.assertTrue(hasattr(result, "message_subtype"))
        self.assertTrue(hasattr(result, "message_title"))
        self.assertTrue(hasattr(result, "message_body"))
        self.assertTrue(hasattr(result, "created"))

    @pytest.mark.model
    def test_push_subscription_model(self):
        self.assertEqual(PushSubscriptionModel.query.count(), 1)
        result = PushSubscriptionModel.query.get(self.push_subscription_model.id)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "endpoint"))
        self.assertTrue(hasattr(result, "auth_keys"))
        self.assertTrue(hasattr(result, "subscription_time"))
        self.assertTrue(hasattr(result, "message_id"))
        self.assertTrue(hasattr(result, "delivered_to_device"))
        self.assertTrue(hasattr(result, "time_delivered"))

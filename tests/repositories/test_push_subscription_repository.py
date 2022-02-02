import pytest

from app.models import PushSubscriptionModel
from tests.base_test_case import BaseTestCase


class TestPushMessageRepository(BaseTestCase):
    @pytest.mark.repository
    def test_create(self):
        self.assertEqual(PushSubscriptionModel.query.count(), 1)
        result = self.push_subscription_repository.create(
            self.push_subscription_test_data.new_subscription
        )
        self.assertTrue(result, PushSubscriptionModel)
        self.assertEqual(PushSubscriptionModel.query.count(), 2)

    @pytest.mark.repository
    def test_index(self):
        result = self.push_subscription_repository.index()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    @pytest.mark.repository
    def test_find(self):
        result = self.push_subscription_repository.find(
            {
                "endpoint": self.push_subscription_model.endpoint,
            }
        )
        self.assertIsNotNone(result)

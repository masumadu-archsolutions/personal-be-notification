import pytest

from app.models import SMSModel
from tests import BaseTestCase


class TestSMSNotificationModels(BaseTestCase):
    @pytest.mark.model
    def test_sms_model(self):
        self.assertEqual(SMSModel.query.count(), 1)
        sms = SMSModel.query.get(self.sms_model.id)
        self.assertIsInstance(sms, SMSModel)
        self.assertTrue(hasattr(sms, "id"))
        self.assertTrue(hasattr(sms, "recipient"))
        self.assertTrue(hasattr(sms, "message_type"))
        self.assertTrue(hasattr(sms, "message"))
        self.assertTrue(hasattr(sms, "reference"))
        self.assertTrue(hasattr(sms, "sms_client"))
        self.assertTrue(hasattr(sms, "delivered_to_sms_client"))

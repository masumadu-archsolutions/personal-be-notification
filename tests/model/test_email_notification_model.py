import pytest

from app.models import EmailModel
from tests import BaseTestCase


class TestEmailNotificationModels(BaseTestCase):
    @pytest.mark.model
    def test_sms_model(self):
        self.assertEqual(EmailModel.query.count(), 1)
        email = EmailModel.query.get(self.email_model.id)
        self.assertIsInstance(email, EmailModel)
        self.assertTrue(hasattr(email, "id"))
        self.assertTrue(hasattr(email, "recipient"))
        self.assertTrue(hasattr(email, "email_client"))
        self.assertTrue(hasattr(email, "message_type"))
        self.assertTrue(hasattr(email, "message_subtype"))
        self.assertTrue(hasattr(email, "reference"))
        self.assertTrue(hasattr(email, "email_client"))
        self.assertTrue(hasattr(email, "delivered_to_email_client"))
        self.assertTrue(hasattr(email, "created"))

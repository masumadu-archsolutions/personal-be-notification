import pytest

from app.models import NotificationTemplateModel
from tests import BaseTestCase


class TestModels(BaseTestCase):
    @pytest.mark.model
    def test_notification_template_model(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 2)
        template = NotificationTemplateModel.query.get(self.sms_template_test_model.id)
        self.assertTrue(hasattr(template, "id"))
        self.assertTrue(hasattr(template, "type"))
        self.assertTrue(hasattr(template, "subtype"))
        self.assertTrue(hasattr(template, "template_file"))
        self.assertTrue(hasattr(template, "keywords"))
        self.assertIsInstance(template.keywords, list)
        self.assertTrue(hasattr(template, "created"))
        self.assertTrue(hasattr(template, "modified"))

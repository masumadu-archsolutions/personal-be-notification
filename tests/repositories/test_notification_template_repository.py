import uuid

import pytest

from app.core.exceptions import AppException
from app.models import NotificationTemplateModel
from tests.base_test_case import BaseTestCase


class TestNotificationTemplateRepository(BaseTestCase):
    @pytest.mark.repository
    def test_create(self):
        template = self.template_repository.create(self.template_test_data.new_template)
        self.assertTrue(template, NotificationTemplateModel)
        self.assertEqual(NotificationTemplateModel.query.count(), 3)
        with self.assertRaises(AppException.OperationError) as duplicate_template:
            self.template_repository.create(self.template_test_data.new_template)
        self.assertTrue(duplicate_template.exception)
        self.assert500(duplicate_template.exception)

    @pytest.mark.repository
    def test_find_by_id(self):
        template = self.template_repository.find_by_id(self.sms_template_test_model.id)
        self.assertIsNotNone(template)
        self.assertTrue(template, NotificationTemplateModel)
        self.assertTrue(template, self.sms_template_test_model)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.template_repository.find_by_id(uuid.uuid4())
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

    @pytest.mark.repository
    def test_find(self):
        template = self.template_repository.find(
            {
                "type": self.sms_template_test_model.type,
                "subtype": self.sms_template_test_model.subtype,
            }
        )
        self.assertIsNotNone(template)
        self.assertEqual(template, self.sms_template_test_model)

    @pytest.mark.repository
    def test_find_all(self):
        template = self.template_repository.find_all(
            {"type": self.sms_template_test_model.type}
        )
        self.assertIsNotNone(template)
        self.assertIsInstance(template, list)

    @pytest.mark.repository
    def test_update(self):
        template = self.template_repository.update_by_id(
            self.sms_template_test_model.id, self.template_test_data.update_template
        )
        self.assertIsNotNone(template)
        self.assertEqual(
            template.keywords, self.template_test_data.update_template.get("keywords")
        )

    @pytest.mark.repository
    def test_delete(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 2)
        template_id = self.sms_template_test_model.id
        template = self.template_repository.delete(template_id)
        self.assertIsNone(template)
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.template_repository.find_by_id(template_id)
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

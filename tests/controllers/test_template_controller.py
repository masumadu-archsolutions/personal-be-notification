import uuid

import pytest

from app.core.exceptions import AppException
from app.core.result import Result
from app.models import NotificationTemplateModel
from tests import BaseTestCase


class TestTemplateController(BaseTestCase):
    @pytest.mark.controller
    def test_index(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        get_all_templates = self.template_controller.index()
        self.assertIsInstance(get_all_templates, Result)
        self.assertEqual(get_all_templates.status_code, 200)
        self.assertIsInstance(get_all_templates.value, list)

    @pytest.mark.controller
    def test_show(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        get_template = self.template_controller.show(self.template_test_model.id)
        self.assertIsNotNone(get_template)
        self.assertIsInstance(get_template, Result)
        self.assertEqual(get_template.status_code, 200)
        self.assertIsInstance(get_template.value, NotificationTemplateModel)
        self.assertEqual(get_template.value, self.template_test_model)
        with self.assertRaises(AppException.NotFoundException) as not_found_exc:
            self.template_controller.show(uuid.uuid4())
        self.assertTrue(not_found_exc.exception)
        self.assert404(not_found_exc.exception)

    @pytest.mark.controller
    def test_create(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        template = self.template_controller.create(self.template_test_data.new_template)
        self.assertIsNotNone(template)
        self.assertEqual(NotificationTemplateModel.query.count(), 2)
        self.assertIsInstance(template, Result)
        self.assertEqual(template.status_code, 201)
        self.assertIsInstance(template.value, NotificationTemplateModel)
        with self.assertRaises(AppException.OperationError) as operation_exc:
            self.template_controller.create(self.template_test_data.new_template)
        self.assertTrue(operation_exc.exception)
        self.assert500(operation_exc.exception)

    @pytest.mark.controller
    def test_update(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        template = self.template_controller.update(
            self.template_test_model.id, self.template_test_data.update_template
        )

        self.assertIsInstance(template, Result)
        self.assertEqual(template.status_code, 200)
        self.assertNotEqual(
            template.value.type, self.template_test_data.existing_template.get("type")
        )
        self.assertNotEqual(
            template.value.keywords,
            self.template_test_data.existing_template.get("keywords"),
        )
        self.assertIsInstance(template.value, NotificationTemplateModel)
        with self.assertRaises(AppException.NotFoundException) as not_found_exc:
            self.template_controller.update(
                uuid.uuid4(), self.template_test_data.update_template
            )
        self.assertTrue(not_found_exc.exception)
        self.assert404(not_found_exc.exception)

    @pytest.mark.controller
    def test_delete(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        with self.assertRaises(AppException.NotFoundException) as not_found_exc:
            self.template_controller.delete(uuid.uuid4())
        self.assertTrue(not_found_exc.exception)
        self.assert404(not_found_exc.exception)
        template = self.template_controller.delete(self.template_test_model.id)
        self.assertIsInstance(template, Result)
        self.assertEqual(template.status_code, 204)

import pytest
from flask import url_for

from app.models import NotificationTemplateModel
from tests import BaseTestCase


class TestSMSView(BaseTestCase):
    @pytest.mark.views
    def test_create_template(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        with self.client:
            response = self.client.post(
                url_for("template.create_template"),
                json=self.template_test_data.new_template,
            )
            self.assertEqual(NotificationTemplateModel.query.count(), 2)
            response_data = response.json
            self.assertStatus(response, 201)
            self.assertIsInstance(response_data, dict)

    @pytest.mark.views
    def test_get_all_templates(self):
        with self.client:
            response = self.client.get(url_for("template.get_all_templates"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, list)

    @pytest.mark.views
    def test_get_template(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        with self.client:
            response = self.client.get(
                url_for("template.get_template", template_id=self.template_test_model.id)
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)

    @pytest.mark.active
    def test_update_template(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        template = NotificationTemplateModel.query.get(self.template_test_model.id)
        self.assertIsInstance(template, NotificationTemplateModel)
        self.assertEqual(template.type, "sms_notification")
        with self.client:
            response = self.client.patch(
                url_for("template.update_template", template_id=template.id),
                json=self.template_test_data.update_template,
            )
            response_data = response.json
            self.assertStatus(response, 200)
            self.assertIsInstance(response_data, dict)
            self.assertEqual(
                self.template_test_data.update_template.get("type"),
                response_data.get("type"),
            )
            self.assertEqual(
                self.template_test_data.update_template.get("keywords"),
                response_data.get("keywords"),
            )

    @pytest.mark.views
    def test_delete_template(self):
        self.assertEqual(NotificationTemplateModel.query.count(), 1)
        template = NotificationTemplateModel.query.get(self.template_test_model.id)
        self.assertIsNotNone(template)
        self.assertIsInstance(template, NotificationTemplateModel)
        with self.client:
            response = self.client.delete(
                url_for("template.delete_template", template_id=template.id)
            )
            self.assertEqual(response.status_code, 204)
            self.assertEqual(NotificationTemplateModel.query.count(), 0)

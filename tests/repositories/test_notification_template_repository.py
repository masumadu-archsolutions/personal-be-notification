# from app.core.exceptions import AppException
from tests.base_test_case import BaseTestCase
import pytest


class TestNotificationTemplateRepository(BaseTestCase):
    # pass
    @pytest.mark.active
    def test_create(self):
        self.assertEqual(self.template.subtype, self.subtype)

    # #
    # def test_find_by_id(self):
    #     template = self.template
    #     response = self.template_repository.find_by_id(template.id)
    #     self.assertEqual(template, response)
    #
    # def test_find(self):
    #     template = self.template
    #     response = self.template_repository.find(
    #         {"type": "sms_notification", "subtype": "daily_greeting"}
    #     )
    #     self.assertEqual(response.type, "sms_notification")
    #     self.assertEqual(response.subtype, "daily_greeting")
    #     self.assertEqual(response.id, template.id)
    #
    # def test_update(self):
    #     template = self.template
    #     new_message = "Hello {{username}}, today is another day to be great"
    #     response = self.template_repository.update_by_id(
    #         template.id, {"message": new_message}
    #     )
    #
    #     self.assertEqual(response.message, new_message)
    #
    # def test_delete(self):
    #     template = self.template
    #     self.template_repository.delete(template.id)
    #     with self.assertRaises(AppException.NotFoundException):
    #         self.template_repository.find_by_id(template.id)

    # TODO: write tests for duplicate sms templates

import uuid

import pytest

from app.core.exceptions import AppException
from app.models import PushMessageModel
from tests.base_test_case import BaseTestCase


class TestPushMessageRepository(BaseTestCase):
    @pytest.mark.repository
    def test_create(self):
        result = self.push_message_repository.create(
            self.push_message_test_data.new_message
        )
        self.assertTrue(result, PushMessageModel)
        self.assertEqual(PushMessageModel.query.count(), 2)
        with self.assertRaises(AppException.OperationError) as duplicate_message:
            self.push_message_repository.create(self.push_message_test_data.new_message)
        self.assertTrue(duplicate_message.exception)
        self.assert500(duplicate_message.exception)

    @pytest.mark.repository
    def test_find_by_id(self):
        result = self.push_message_repository.find_by_id(self.push_message_model.id)
        self.assertIsNotNone(result)
        self.assertTrue(result, PushMessageModel)
        self.assertTrue(result, self.push_message_model)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.push_message_repository.find_by_id(uuid.uuid4())
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

    @pytest.mark.repository
    def test_find(self):
        result = self.push_message_repository.find(
            {
                "message_type": self.push_message_model.message_type,
                "message_subtype": self.push_message_model.message_subtype,
            }
        )
        self.assertIsNotNone(result)
        self.assertEqual(result, self.push_message_model)

    @pytest.mark.repository
    def test_find_all(self):
        result = self.push_message_repository.find_all(
            {"message_type": self.push_message_model.message_type}
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    @pytest.mark.repository
    def test_update(self):
        result = self.push_message_repository.update_by_id(
            self.push_message_model.id, self.push_message_test_data.update_message
        )
        self.assertIsNotNone(result)
        self.assertEqual(
            result.message_body,
            self.push_message_test_data.update_message.get("message_body"),
        )

    @pytest.mark.repository
    def test_delete(self):
        self.assertEqual(PushMessageModel.query.count(), 1)
        message_id = self.push_message_model.id
        result = self.push_message_repository.delete(message_id)
        self.assertIsNone(result)
        self.assertEqual(PushMessageModel.query.count(), 0)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.push_message_repository.find_by_id(message_id)
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

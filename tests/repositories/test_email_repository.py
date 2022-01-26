import uuid

import pytest

from app.core.exceptions import AppException
from app.models import EmailModel
from tests.base_test_case import BaseTestCase


class TestEmailRepository(BaseTestCase):
    @pytest.mark.repository
    def test_create(self):
        email = self.email_repository.create(self.email_test_data.existing_email)
        self.assertTrue(email, EmailModel)
        self.assertEqual(EmailModel.query.count(), 2)

    @pytest.mark.repository
    def test_find_by_id(self):
        email = self.email_repository.find_by_id(self.email_model.id)
        self.assertTrue(email, EmailModel)
        self.assertTrue(email, self.email_model)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.email_repository.find_by_id(uuid.uuid4())
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

    @pytest.mark.repository
    def test_find(self):
        email = self.email_repository.find(
            {
                "recipient": self.email_model.recipient,
                "message_subtype": self.email_model.message_subtype,
            }
        )
        self.assertIsNotNone(email)
        self.assertEqual(email, self.email_model)

    @pytest.mark.repository
    def test_find_all(self):
        email = self.email_repository.find_all({"recipient": self.email_model.recipient})
        self.assertIsNotNone(email)
        self.assertIsInstance(email, list)

    @pytest.mark.repository
    def test_delete(self):
        self.assertEqual(EmailModel.query.count(), 1)
        email_id = self.email_model.id
        email = self.email_repository.delete(email_id)
        self.assertIsNone(email)
        self.assertEqual(EmailModel.query.count(), 0)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.email_repository.find_by_id(email_id)
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

import uuid

import pytest

from app.core.exceptions import AppException
from app.models import SMSModel
from tests.base_test_case import BaseTestCase


class TestSMSRepository(BaseTestCase):
    @pytest.mark.repository
    def test_create(self):
        sms = self.sms_repository.create(self.sms_test_data.existing_sms)
        self.assertTrue(sms, SMSModel)
        self.assertEqual(SMSModel.query.count(), 2)

    @pytest.mark.repository
    def test_find_by_id(self):
        sms = self.sms_repository.find_by_id(self.sms_model.id)
        self.assertTrue(sms, SMSModel)
        self.assertTrue(sms, self.sms_model)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.sms_repository.find_by_id(uuid.uuid4())
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

    @pytest.mark.repository
    def test_find(self):
        sms = self.sms_repository.find(
            {
                "recipient": self.sms_model.recipient,
                "message_subtype": self.sms_model.message_subtype,
            }
        )
        self.assertIsNotNone(sms)
        self.assertEqual(sms, self.sms_model)

    @pytest.mark.repository
    def test_find_all(self):
        sms = self.sms_repository.find_all({"recipient": self.sms_model.recipient})
        self.assertIsNotNone(sms)
        self.assertIsInstance(sms, list)

    @pytest.mark.repository
    def test_delete(self):
        self.assertEqual(SMSModel.query.count(), 1)
        sms_id = self.sms_model.id
        sms = self.sms_repository.delete(sms_id)
        self.assertIsNone(sms)
        self.assertEqual(SMSModel.query.count(), 0)
        with self.assertRaises(AppException.NotFoundException) as not_found:
            self.sms_repository.find_by_id(sms_id)
        self.assertTrue(not_found.exception)
        self.assert404(not_found.exception)

import pytest
from flask import url_for

from app.models import SMSModel
from tests import BaseTestCase


class TestSMSView(BaseTestCase):
    @pytest.mark.views
    def test_get_all_sms(self):
        self.assertEqual(SMSModel.query.count(), 1)
        with self.client:
            response = self.client.get(url_for("sms.get_all_sms"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, list)

    @pytest.mark.views
    def test_get_sms(self):
        self.assertEqual(SMSModel.query.count(), 1)
        with self.client:
            response = self.client.get(url_for("sms.get_sms", sms_id=self.sms_model.id))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)

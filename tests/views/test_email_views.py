import pytest
from flask import url_for

from app.models import EmailModel
from tests import BaseTestCase


class TestEmailView(BaseTestCase):
    @pytest.mark.views
    def test_get_all_email(self):
        self.assertEqual(EmailModel.query.count(), 1)
        with self.client:
            response = self.client.get(url_for("email.get_all_email"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, list)

    @pytest.mark.views
    def test_get_email(self):
        self.assertEqual(EmailModel.query.count(), 1)
        with self.client:
            response = self.client.get(
                url_for("email.get_email", email_id=self.email_model.id)
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)

from unittest import mock

import pytest
from flask import url_for

from app.models import PushMessageModel, PushSubscriptionModel
from tests import BaseTestCase


class TestEmailView(BaseTestCase):
    @pytest.mark.views
    def test_create_message(self):
        with self.client:
            response = self.client.post(
                url_for("push.create_message"),
                json=self.push_message_test_data.new_message,
            )
            response_data = response.json
            self.assertEqual(response.status_code, 201)
            self.assertIsInstance(response_data, dict)
            self.assertEqual(PushMessageModel.query.count(), 2)

    @pytest.mark.views
    def test_get_all_messages(self):
        with self.client:
            response = self.client.get(url_for("push.get_all_messages"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, list)

    @pytest.mark.views
    def test_get_message(self):
        with self.client:
            response = self.client.get(
                url_for("push.get_message", message_id=self.push_message_model.id)
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)

    @pytest.mark.views
    def test_update_message(self):
        with self.client:
            response = self.client.patch(
                url_for("push.update_message", message_id=self.push_message_model.id),
                json=self.push_message_test_data.update_message,
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)
            self.assertNotEqual(
                response_data.get("message_body"),
                self.push_message_test_data.existing_message.get("message_body"),
            )

    @pytest.mark.views
    def test_delete_message(self):
        with self.client:
            response = self.client.delete(
                url_for("push.delete_message", message_id=self.push_message_model.id)
            )
            self.assertEqual(response.status_code, 204)
            self.assertEqual(PushMessageModel.query.count(), 0)

    @pytest.mark.views
    def test_subscribe(self):
        with self.client:
            response = self.client.post(
                url_for("push.subscribe"),
                json=self.push_subscription_test_data.new_subscription,
            )
            response_data = response.json
            self.assertEqual(response.status_code, 201)
            self.assertIsInstance(response_data, dict)
            self.assertEqual(PushSubscriptionModel.query.count(), 2)

    @pytest.mark.views
    def test_get_all_subscription(self):
        with self.client:
            response = self.client.get(url_for("push.get_all_subscriptions"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, list)

    @pytest.mark.views
    def test_get_subscription_messages(self):
        with self.client:
            response = self.client.get(url_for("push.get_subscription_messages"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, list)

    @pytest.mark.views
    @mock.patch("app.tasks.push_task.send_push.delay")
    def test_send_message(self, mock_delay):
        with self.client:
            response = self.client.post(
                url_for("push.send_message"),
                json=self.push_subscription_test_data.send_push_request,
            )

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, dict)
            self.assertIn("status", response.json)

    @pytest.mark.views
    def test_send_server_id(self):
        with self.client:
            response = self.client.get(url_for("push.send_server_id"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)
            self.assertIn("public_key", response_data)

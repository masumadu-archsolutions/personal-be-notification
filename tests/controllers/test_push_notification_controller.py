import uuid
from unittest import mock

import pytest

from app.core.exceptions import AppException
from app.core.result import Result
from app.models import PushMessageModel, PushSubscriptionModel
from tests import BaseTestCase


class TestPushNotificationController(BaseTestCase):
    @pytest.mark.controller
    def test_create_message(self):
        result = self.push_controller.create_message(
            self.push_message_test_data.new_message
        )
        self.assertIsNotNone(result)
        self.assertEqual(PushMessageModel.query.count(), 2)
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 201)
        self.assertIsInstance(result.value, PushMessageModel)
        with self.assertRaises(AppException.OperationError) as operation_exc:
            self.push_controller.create_message(self.push_message_test_data.new_message)
        self.assertTrue(operation_exc.exception)
        self.assert500(operation_exc.exception)

    @pytest.mark.controller
    def test_show_all_message(self):
        result = self.push_controller.show_all_messages()
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(result.value, list)

    @pytest.mark.controller
    def test_show_message(self):
        result = self.push_controller.show_message(self.push_message_model.id)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(result.value, PushMessageModel)
        self.assertEqual(result.value, self.push_message_model)
        with self.assertRaises(AppException.NotFoundException) as not_found_exc:
            self.push_controller.show_message(uuid.uuid4())
        self.assertTrue(not_found_exc.exception)
        self.assert404(not_found_exc.exception)

    @pytest.mark.controller
    def test_update_message(self):
        result = self.push_controller.update_message(
            self.push_message_model.id, self.push_message_test_data.update_message
        )
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(
            result.value.message_body,
            self.push_message_test_data.existing_message.get("message_body"),
        )
        self.assertIsInstance(result.value, PushMessageModel)
        with self.assertRaises(AppException.NotFoundException) as not_found_exc:
            self.push_controller.update_message(
                uuid.uuid4(), self.push_message_test_data.update_message
            )
        self.assertTrue(not_found_exc.exception)
        self.assert404(not_found_exc.exception)

    @pytest.mark.controller
    def test_delete_message(self):
        self.assertEqual(PushMessageModel.query.count(), 1)
        message = self.push_controller.show_message(self.push_message_model.id)
        result = self.push_controller.delete_message(message.value.id)
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 204)
        with self.assertRaises(AppException.NotFoundException) as not_found_exc:
            self.push_controller.delete_message(message.value.id)
        self.assertTrue(not_found_exc.exception)
        self.assert404(not_found_exc.exception)

    @pytest.mark.controller
    def test_subscribe_user(self):
        result = self.push_controller.subscribe_user(
            self.push_subscription_test_data.new_subscription
        )
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 201)
        self.assertIsInstance(result.value, PushSubscriptionModel)

    @pytest.mark.controller
    def test_show_all_subscription(self):
        result = self.push_controller.show_all_subscriptions()
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(result.value, list)

    @pytest.mark.controller
    def test_show_subscription(self):
        result = self.push_controller.show_subscription(self.push_subscription_model.id)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(result.value, PushSubscriptionModel)
        self.assertEqual(result.value, self.push_subscription_model)
        with self.assertRaises(AppException.NotFoundException) as not_found_exc:
            self.push_controller.show_subscription(uuid.uuid4())
        self.assertTrue(not_found_exc.exception)
        self.assert404(not_found_exc.exception)

    @pytest.mark.controller
    def test_server_id(self):
        result = self.push_controller.server_id()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        self.assertEqual(result.status_code, 200)
        self.assertIn("public_key", result.value)

    @pytest.mark.controller
    @mock.patch("app.init_celery")
    def test_send_push(self, mock_celery):
        mock_celery.side_effect = self.init_celery
        with mock.patch("app.tasks.push_task.send_push.delay") as mock_delay:
            result = self.push_controller.send_push(
                self.push_subscription_test_data.send_push_request
            )
            mock_delay.assert_called()
            self.assertIsNotNone(result)
            self.assertIsInstance(result, Result)
            self.assertEqual(result.status_code, 200)
            self.assertIsInstance(result.value, dict)
            self.assertIn("status", result.value)
            with self.assertRaises(AppException.NotFoundException) as not_found:
                self.push_controller.send_push(
                    self.push_subscription_test_data.send_push_request_exc
                )
            self.assertTrue(not_found.exception)
            self.assert404(not_found.exception)

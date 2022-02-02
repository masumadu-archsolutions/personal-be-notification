import json

from loguru import logger

from app.core.exceptions import AppException
from app.core.result import Result
from app.repositories import PushMessageRepository, PushSubscriptionRepository
from app.services import PushService
from config import Config


class PushNotificationController:
    def __init__(
        self,
        push_subscription_repository: PushSubscriptionRepository,
        push_message_repository: PushMessageRepository,  # noqa
        push_service: PushService,
    ):
        self.push_subscription_repository = push_subscription_repository
        self.push_message_repository = push_message_repository
        self.push_service = push_service

    def create_message(self, data):
        try:
            result = self.push_message_repository.create(data)
        except AppException.OperationError as e:
            raise AppException.OperationError(
                context={"controller.create_message": e.context}
            )
        return Result(result, 201)

    def show_all_messages(self):
        result = self.push_message_repository.index()
        return Result(result, 200)

    def show_message(self, obj_id):
        assert obj_id, "missing id of message to find"
        try:
            result = self.push_message_repository.find_by_id(obj_id)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(
                context={
                    "controller.show_message": f"message with id {obj_id} does not exists"
                }
            )
        return Result(result, 200)

    def update_message(self, message_id, message_data):
        try:
            result = self.push_message_repository.update_by_id(message_id, message_data)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(
                context={
                    "controller.update_message": f"push message with id {message_id} does not exists"  # noqa
                }
            )
        return Result(result, 200)

    def delete_message(self, message_id):
        try:
            self.push_message_repository.delete(message_id)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(
                context={
                    "controller.delete_message": f"push message with id {message_id} does not exists"  # noqa
                }
            )
        return Result({}, 204)

    def subscribe_user(self, data):
        endpoint = data.get("endpoint")
        device_info = self.push_subscription_repository.find({"endpoint": endpoint})
        if not device_info:
            result = self.push_subscription_repository.create(data)
            return Result(result, 201)
        return self.show_subscription(device_info.id)

    def show_all_subscriptions(self):
        result = self.push_subscription_repository.index()
        return Result(result, 200)

    def show_subscription(self, push_id):
        assert push_id, "missing id of device to find"
        try:
            result = self.push_subscription_repository.find_by_id(push_id)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(
                context={
                    "controller.show_subscription": f"device with id {push_id} does not exists"
                }
            )
        return Result(result, 200)

    def server_id(self):
        server_id = {"public_key": Config.VAPID_PUBLIC_KEY}
        return Result(server_id, 200)

    def send_push(self, data):
        from app.tasks.push_task import send_push

        """
        this method takes a data that consists of the device id,
        the details of the message and fires a push notification
        on the parameters passed to it.

        e.g of the data structure is:
        {
            "endpoint": "device_id",
            "meta": {
                "message_type": "push_notification",
                "message_subtype": "general"
            }
        }
        based on this information, a message that has already been created in
        the database matching the meta dictionary will be retrieved and its content will
        be sent to the user with the specified device id. For instance, if a message
        "transaction alert, a transaction has occurred on your account" with type and
        subtype that matches the meta is found in the database, that message will be
        sent".When a push is delivered to the specified device email, a
        delivered_to_device flag set on the record will be toggled to true

        """
        endpoint = data.get("endpoint")
        metadata = data.get("metadata")
        result = self.push_subscription_repository.find({"endpoint": endpoint})
        if not result:
            raise AppException.NotFoundException(
                context={"controller.send_push": "device id does not exist"}
            )
        generated_message = self.generate_message(meta=metadata)
        if generated_message:
            subscription_info = {
                "endpoint": result.endpoint,
                "keys": json.loads(result.auth_keys),
            }
            push_data = {
                "subscription_info": subscription_info,
                "message": generated_message,
                "endpoint_id": result.id,
            }
            send_push.delay(
                push_data,
                self.push_service.__class__.__name__,
                self.push_subscription_repository.__class__.__name__,
            )
            return Result({"status": "success"}, 200)
        return Result({"status": "error"}, 500)

    def generate_message(self, meta):
        push_message = self.push_message_repository.find(meta)
        if not push_message:
            logger.error(
                "push_message_error: No message available for this type of push"
            )
            return None

        return {
            "message_id": push_message.id,
            "message_title": push_message.message_title,
            "message_body": push_message.message_body,
        }

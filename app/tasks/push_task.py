import json

from app.celery_app import celery
from app.core.exceptions import AppException
from app.repositories import PushSubscriptionRepository
from app.services import PushService

push_service_instance = PushService()
push_repository_instance = PushSubscriptionRepository()


def service_map(service):
    push_map = {
        push_service_instance.__class__.__name__: push_service_instance,
        push_repository_instance.__class__.__name__: push_repository_instance,
    }

    return push_map.get(service)


@celery.task
def send_push(data, service_name, repository_name):
    """
    :param data: {dict} data to be used to perform action
    :param service_name: {PushServiceInterface} the push service that should be
    used in performing this action
    :param repository_name: {PushSubscriptionRepository} the push repository that should store
    the message record
    """
    push_service = service_map(service_name)
    push_repository = service_map(repository_name)

    subscription_info = data.get("subscription_info")
    message = data.get("message")
    message_id = message.get("message_id")
    endpoint_id = data.get("endpoint_id")
    try:

        push_service.send(
            subscription_info=subscription_info, message=json.dumps(message)
        )
        push_repository.update_by_id(
            endpoint_id,
            {
                "message_id": message_id,
                "delivered_to_device": True,
            },
        )
    except AppException.OperationError:
        push_repository.update_by_id(
            endpoint_id, {"message_id": message_id, "delivered_to_device": False}
        )

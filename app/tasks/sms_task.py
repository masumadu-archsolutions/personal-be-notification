from app.definitions.exceptions import AppException
from app.extensions import celery
from app.repositories import SmsRepository
from app.services import SmsService


sms_service_instance = SmsService()
sms_repository_instance = SmsRepository()


def service_map(service):
    sms_map = {
        sms_service_instance.__class__.__name__: sms_service_instance,
        sms_repository_instance.__class__.__name__: sms_repository_instance,
    }

    return sms_map.get(service)


@celery.task
def send_sms(data, service_name, repository_name):
    """
    :param data: {dict} data to be used to perform action
    :param service_name: {SMSServiceInterface} the sms service that should be
    used in performing this action
    :param repository_name: {SmsRepository} the sms repository that should store
    the sms record
    """
    sms_service = service_map(service_name)
    sms_repository = service_map(repository_name)

    sender = data.get("sender")
    receiver = data.get("recipient")
    message = data.get("message")
    message_id = data.get("message_id")
    try:
        result = sms_service.send(sender, receiver, message)
        sms_repository.update_by_id(
            message_id,
            {
                "reference": result.get("reference"),
                "delivered_to_sms_client": True,
                "sms_client": sms_service.client,
            },
        )
    except AppException.OperationError:
        sms_repository.update_by_id(message_id, {"sms_client": sms_service.client})

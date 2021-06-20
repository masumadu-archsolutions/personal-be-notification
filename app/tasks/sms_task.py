from app.definitions.exceptions import AppException
from app.extensions import celery


@celery.task
def send_sms(data, sms_service, sms_repository):
    """

    """
    sender = data.get("sender")
    receiver = data.get("receiver")
    message = data.get("message")
    message_id = data.get("message_id")
    try:
        result = sms_service.send(sender, receiver, message)
        sms_repository.update_by_id(message_id, {
            "reference": result.get("reference"),
            "delivered_to_sms_client": True,
            "sms_client": sms_service.client
        })
    except AppException.OperationError:
        pass




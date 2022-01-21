from app.celery_app import celery
from app.core.exceptions import AppException
from app.repositories import EmailRepository
from app.services import EmailService

email_service_instance = EmailService()
email_repository_instance = EmailRepository()


def service_map(service):
    email_map = {
        email_service_instance.__class__.__name__: email_service_instance,
        email_repository_instance.__class__.__name__: email_repository_instance,
    }

    return email_map.get(service)


@celery.task
def send_email(data, service_name, repository_name):
    """
    :param data: {dict} data to be used to perform action
    :param service_name: {EmailServiceInterface} the email service that should be
    used in performing this action
    :param repository_name: {EmailRepository} the email repository that should store
    the email record
    """
    email_service = service_map(service_name)
    email_repository = service_map(repository_name)

    recipients = data.get("recipient")
    message = data.get("message")
    message_id = data.get("message_id")
    try:
        email_service.send(recipients=recipients, text_body="lja", html_body=message)
        email_repository.update_by_id(
            message_id,
            {
                "reference": 'result.get("reference")',
                "delivered_to_email_client": True,
                "email_client": email_service.client,
            },
        )
    except AppException.OperationError:
        email_repository.update_by_id(message_id, {"email_client": email_service.client})

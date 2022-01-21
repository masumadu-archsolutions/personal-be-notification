from loguru import logger
from requests.exceptions import RequestException
from sendgrid import Mail, SendGridAPIClient

from app.core.exceptions import AppException
from app.core.service_interfaces import EmailServiceInterface
from config import Config


class EmailService(EmailServiceInterface):
    client = "sendgrid"

    def send(self, recipients, text_body, html_body):
        assert recipients, "Recipients cannot be None"
        assert text_body, "Text body cannot be None"
        assert html_body, "Html body cannot be None"

        try:
            sg = SendGridAPIClient(api_key=Config.EMAIL_CLIENT_API)
            data = {
                "from_email": "michaelasumadu1@outlook.com",
                "to_emails": recipients,
                "subject": "none",
                "html_content": html_body,
            }
            msg = Mail(**data)
            sg.send(msg)
            logger.info("message sent successfully to email provider")
            # return {"reference": data.get("messageId")}
        except RequestException as exc:
            logger.error(
                f"error sending message to email provider with error message {exc.args[0]}"
            )
            raise AppException.OperationError(context="Error sending email")

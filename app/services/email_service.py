from bs4 import BeautifulSoup

# from flask_mail import Message
from loguru import logger
from sendgrid import Mail, SendGridAPIClient, SendGridException

# from app import mail
from app.core.exceptions import AppException
from app.core.service_interfaces import EmailServiceInterface
from config import Config


class EmailService(EmailServiceInterface):
    client = "sendgrid"

    def send(
        self, subject=None, sender=None, recipients=None, text_body=None, html_body=None
    ):
        assert recipients, "Recipients cannot be None"
        assert html_body, "Html body cannot be None"

        try:
            sg = SendGridAPIClient(api_key=Config.EMAIL_CLIENT_API)
            data = {
                "from_email": Config.MAIL_DEFAULT_SENDER,
                "to_emails": recipients,
                "subject": self.mail_subject(html_body),
                "plain_text_content": self.mail_text_body(html_body),
                "html_content": html_body,
            }
            msg = Mail(**data)
            # self.send_mail()
            sg.send(msg)
            logger.info("message sent successfully to email provider")
            # return {"reference": data.get("messageId")}
        except SendGridException as exc:
            logger.error(
                f"error sending message to email provider with error message {exc.args}"
            )
            raise AppException.OperationError(context="Error sending email")

    # def send_mail(self):
    #     msg = Message(
    #         subject="Testing flask mail Configuration",
    #         sender="michaelasumadu1@gmail.com",
    #         recipients=["michaelasumadu10@gmail.com"],
    #         body="this is the body",
    #         html="<h1>the body </h1>",
    #     )
    #     mail.send(msg)

    def mail_subject(self, html_body):
        soup = BeautifulSoup(html_body, features="html.parser")
        subject = soup.find("meta", attrs={"name": "subject"})
        if subject:
            return subject["content"]
        return " "

    def mail_text_body(self, html_body):
        soup = BeautifulSoup(html_body, features="html.parser")
        text_body = soup.get_text().strip()
        return text_body

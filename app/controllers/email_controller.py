import os
import re

from flask import render_template
from loguru import logger

from app.core.result import Result
from app.repositories import EmailRepository, NotificationTemplateRepository
from app.services import EmailService


class EmailController:
    def __init__(
        self,
        email_repository: EmailRepository,
        notification_template_repository: NotificationTemplateRepository,  # noqa
        email_service: EmailService,
    ):
        self.email_repository = email_repository
        self.email_service = email_service
        self.template_repository = notification_template_repository

    def index(self):
        result = self.email_repository.index()
        return Result(result, 200)

    def show(self, email_id):
        email = self.email_repository.find_by_id(email_id)
        return Result(email, 200)

    def send_mail(self, data):
        from app.tasks.email_task import send_email

        """
        this method takes a data that consists of the recipient of the mail,
        the details of the mail and the mail meta and fires an email
        notification based on the parameters
        passed to it.

        e.g of the data structure is:
        {
            "recipient": "example@gmail.com",
            "details": {
                "name": "John",
                "verification_code": "123456"
            },
            "meta": {
                "type": "email_notification",
                "subtype": "general"
            }
        }

        based on this information, a mail template that has already been created in
        the database matching the meta dictionary will be retrieved and its
        placeholders will be replaced with the data in the details key in the data.

        For instance, if a message "Hello {{name}}, your verification code is
        {{verification_code}}" with type and subtype that matches the meta is
        found in the database, the mail constructed will be
        "Hello John, your verification code is 123456"

        Also this method uses celery to run asynchronous tasks so as not to block
        the main thread. if the mail takes too long to be delivered.

        When a mail is delivered to the external email provider,
        a delivered_to_email_client flag set on the record will be toggled to true

        """
        recipient = data.get("recipient")
        details = data.get("details")
        meta = data.get("meta")
        generated_mail = self.generate_mail(details=details, meta=meta)
        if generated_mail:
            email_body = generated_mail.get("email_message")
            message_template = generated_mail.get("message_template")

            email_record_data = {
                "recipient": recipient,
                "message_type": meta.get("type"),
                "message_subtype": meta.get("subtype"),
                "message_template": message_template,
            }
            email_record = self.email_repository.create(email_record_data)
            email_data = {
                "recipient": recipient,
                "email_body": email_body,
                "email_id": email_record.id,
            }
            send_email.delay(
                email_data,
                self.email_service.__class__.__name__,
                self.email_repository.__class__.__name__,
            )

    def generate_mail(self, details, meta):
        message_template = self.template_repository.find(meta)

        if not message_template:
            logger.error("template_error: No template available for this type of email")
            return None
        template_file = message_template.template_file
        template_path = f"email/{template_file}"

        if self.template_file_exist(template_file):
            email_body = render_template(template_path, **details)

            # get keywords from message_template
            keywords = message_template.keywords
            for keyword in keywords:
                is_sensitive = keyword.get("is_sensitive")
                if is_sensitive:
                    item = keyword.get("placeholder")
                    details[item] = re.sub(".", "*", str(details.get(item)))

            redacted_mail = render_template(template_path, **details)

            return {
                "message_template": template_file,
                "email_message": email_body,
                "sanitized_mail": redacted_mail,
            }
        logger.error(f"template_error: template file {template_file} not found")
        return None

    def template_file_exist(self, filename):
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        templates = os.listdir(f"{parent_directory}/templates/email")
        if not filename or filename not in templates:
            return None
        return templates

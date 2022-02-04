import os.path
import re

from flask import render_template
from loguru import logger

from app.core.result import Result
from app.repositories import NotificationTemplateRepository, SmsRepository
from app.services import SmsService


class SmsController:
    def __init__(
        self,
        sms_repository: SmsRepository,
        notification_template_repository: NotificationTemplateRepository,  # noqa
        sms_service: SmsService,
    ):
        self.sms_repository = sms_repository
        self.sms_service = sms_service
        self.template_repository = notification_template_repository

    def index(self):
        result = self.sms_repository.index()
        return Result(result, 200)

    def show(self, sms_id):
        sms = self.sms_repository.find_by_id(sms_id)
        return Result(sms, 200)

    def send_message(self, data):
        from app.tasks.sms_task import send_sms

        """
        this method takes a data that consists of the recipient of the message,
        the details of the message and the message meta and fires an sms
        notification based on the parameters
        passed to it.

        e.g of the data structure is:
        {
            "recipient": "0241112223",
            "details": {
                "name": "John",
                "verification_code": "123456"
            },
            "meta": {
                "type": "sms_notification",
                "subtype": "otp"
            }
        }

        based on this information, a message that has already been created in
        the database matching the meta dictionary will be retrieved and its
        placeholders will be replaced with the data in the details key in the.

        For instance, if a message "Hello {{name}}, your verification code is
        {{verification_code}}" with type and subtype that matches the meta is
        found in the database, the message constructed will be
        "Hello John, your verification code is 123456"

        Also this method uses celery to run asynchronous tasks so as not to block
        the main thread. if the message takes too long to be delivered.

        When a message is delivered to the external sms provider,
        a delivered_to_sms_client flag set on the record will be toggled to true

        """
        recipient = data.get("recipient")
        details = data.get("details")
        meta = data.get("meta")
        generated_message = self.generate_messages(details=details, meta=meta)
        if generated_message:
            sanitized_message = generated_message.get("sanitized_message")
            message = generated_message.get("message")
            message_template = generated_message.get("message_template")

            sms_record_data = {
                "recipient": recipient,
                "message": sanitized_message,
                "message_type": meta.get("type"),
                "message_subtype": meta.get("subtype"),
                "message_template": message_template,
            }
            sms_record = self.sms_repository.create(sms_record_data)
            sms_data = {
                "sender": "Quantum",
                "recipient": recipient,
                "message": message,
                "message_id": sms_record.id,
            }
            send_sms.delay(
                sms_data,
                self.sms_service.__class__.__name__,
                self.sms_repository.__class__.__name__,
            )

    def generate_messages(self, details, meta):
        message_template = self.template_repository.find(meta)

        # check if template exist in database
        if not message_template:
            logger.error("template_error: No template available for this type of sms")
            return None

        template_file = message_template.template_file
        file_path = self.template_file_exist(template_file)
        if file_path:
            message = render_template(file_path, **details)

            # get keywords from message_template
            keywords = message_template.keywords
            for keyword in keywords:
                is_sensitive = keyword.get("is_sensitive")
                if is_sensitive:
                    item = keyword.get("placeholder")
                    details[item] = re.sub(".", "*", str(details.get(item)))

            redacted_message = render_template(file_path, **details)

            return {
                "message": message,
                "sanitized_message": redacted_message,
                "message_template": template_file,
            }
        return None

    def template_file_exist(self, filename):
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        template_file_directory = os.listdir(f"{parent_directory}/templates/sms")
        if not filename or filename not in template_file_directory:
            logger.error(f"template_error: template file {filename} not found")
            return None
        file_path = f"sms/{filename}"
        return file_path

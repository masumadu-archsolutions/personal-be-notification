import re
import json
from jinja2 import Template
from app.definitions.result import Result
from app.definitions.service_result import ServiceResult
from app.repositories import SmsRepository, NotificationTemplateRepository
from app.services import SmsService
from app.tasks.sms_task import send_sms


class SmsController:
    def __init__(
        self,
        sms_repository: SmsRepository,
        notification_template_repository: NotificationTemplateRepository,  # noqa
        sms_service: SmsService,
    ):
        self.repository = sms_repository
        self.sms_service = sms_service
        self.template_repository = notification_template_repository

    def index(self):
        result = self.repository.index()
        return ServiceResult(Result(result, 200))

    def show(self, sms_id):
        sms = self.repository.find_by_id(sms_id)
        return ServiceResult(Result(sms, 200))

    def send_message(self, data):
        recipient = data.get("recipient")
        details = data.get("details")
        meta = data.get("meta")
        generated_message = self.generate_messages(details=details, meta=meta)
        sanitized_message = generated_message.get("sanitized_message")
        message = generated_message.get("message")

        sms_record_data = {
            "recipient": recipient,
            "message": sanitized_message,
            "message_type": meta.get("type"),
        }
        sms_record = self.repository.create(sms_record_data)
        sms_data = {
            "sender": "Quantum",
            "recipient": recipient,
            "message": message,
            "message_id": sms_record.id,
        }
        send_sms.delay(
            sms_data,
            self.sms_service.__class__.__name__,
            self.repository.__class__.__name__,
        )

    def generate_messages(self, details, meta):
        message_template = self.template_repository.find(meta)

        if not message_template:
            return "Empty message"
        template_string = message_template.template
        template = Template(template_string)
        message = template.render(**details)

        # get keywords from message_template
        keywords = json.loads(message_template.keywords)
        for keyword in keywords:
            is_sensitive = keyword.get("is_sensitive")
            if is_sensitive:
                # TODO: change 'keyword' below to 'placeholder' in the database
                item = keyword.get("keyword")
                details[item] = re.sub(".", "*", str(details.get(item)))

        redacted_message = template.render(**details)

        return {"message": message, "sanitized_message": redacted_message}

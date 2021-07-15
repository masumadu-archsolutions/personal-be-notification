from app.definitions.result import Result
from app.definitions.service_result import ServiceResult
from app.models.sms_model import SMSTypeEnum
from app.repositories import SmsRepository
from app.services import SmsService
from app.tasks.sms_task import send_sms


class SmsController:
    def __init__(self, sms_repository: SmsRepository, sms_service: SmsService):
        self.repository = sms_repository
        self.sms_service = sms_service

    def index(self):
        result = self.repository.index()
        return ServiceResult(Result(result, 200))

    def show(self, sms_id):
        sms = self.repository.find_by_id(sms_id)
        return ServiceResult(Result(sms, 200))

    def send_token(self, data):
        """
        controller method to send sms token to customer in order to confirm
        customer's phone number
        :param data: {dict} data containing sender, recipient and token of customer
        """

        recipient = data.get("recipient")
        token = data["message"]
        message = self.token_message(token.get("otp"))
        data = {
            "recipient": recipient,
            "message": self.token_message("******"),
            "message_type": SMSTypeEnum.otp,
        }
        sms = self.repository.create(data)
        sms_data = {
            "sender": "Quantum",
            "recipient": recipient,
            "message": message,
            "message_id": sms.id,
        }
        send_sms.delay(
            sms_data,
            self.sms_service.__class__.__name__,
            self.repository.__class__.__name__,
        )

    def token_message(self, token):
        return f"Your verification code is {token}"

    def send_notification(self, data):
        recipient = data.get("recipient")
        message_data = data.get("message")
        message = message_data.get("message")

        data = {
            "recipient": recipient,
            "message": message,
            "message_type": SMSTypeEnum.notification,
        }

        sms = self.repository.create(data)

        sms_data = {
            "sender": "Quantum",
            "recipient": recipient,
            "message": message,
            "message_id": sms.id,
        }

        send_sms.delay(
            sms_data,
            self.sms_service.__class__.__name__,
            self.repository.__class__.__name__,
        )

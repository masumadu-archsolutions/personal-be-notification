from app.definitions.result import Result
from app.definitions.service_result import ServiceResult
from app.models.sms_model import SMSTypeEnum
from app.repositories import SMSRepository
from app.services import SMSService
from app.tasks.sms_task import send_sms


class SMSController:
    def __init__(self, sms_repository: SMSRepository, sms_service: SMSService):
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

        sender = data["sender"]
        recipient = data["recipient"]
        token = data["token"]
        message = self.token_message(token)
        data = {
            "recipient": recipient,
            "message": self.token_message("******"),
            "message_type": SMSTypeEnum.otp,
        }
        sms = self.repository.create(data)
        sms_data = {
            "sender": sender,
            "recipient": recipient,
            "message": message,
            "message_id": sms.id
        }
        send_sms(sms_data, self.sms_service, self.repository)

    def token_message(self, token):
        return f"Your verification code is {token}"

from config import Config
from requests import request
from requests.exceptions import RequestException

from app.core.exceptions import AppException
from app.core.service_interfaces import SMSServiceInterface


class SmsService(SMSServiceInterface):
    client = "hubtel"
    url = "https://smsc.hubtel.com/v1/messages/send"
    client_id = Config.SMS_CLIENT_ID
    client_secret = Config.SMS_CLIENT_SECRET

    def send(self, sender, receiver, message):
        assert sender, "Sender cannot be None"
        assert receiver, "Receiver cannot be None"
        assert message, "Message cannot be None"

        try:
            request_url = (
                self.url
                + f"?From={sender}&To={receiver}"
                + f"&Content={message}&ClientID={self.client_id}"
                + f"&ClientSecret={self.client_secret}"
                + "&RegisteredDelivery=true"
            )
            result = request("GET", request_url)
            data = result.json()
            return {"reference": data.get("messageId")}
        except RequestException:
            raise AppException.OperationError(context="Error sending sms")

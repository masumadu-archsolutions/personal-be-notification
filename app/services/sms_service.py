import time

from flask import current_app
from requests import request
from requests.exceptions import RequestException

from app.definitions.exceptions import AppException
from app.definitions.service_interfaces import \
    SMSServiceInterface


class SMSService(SMSServiceInterface):
    client = "hubtel"
    url = "https://smsc.hubtel.com/v1/messages/send"
    client_id = current_app.config["SMS_CLIENT_ID"]
    client_secret = current_app.config["SMS_CLIENT_SECRET"]

    def send(self, sender, receiver, message):
        assert sender, "Sender cannot be None"
        assert receiver, "Receiver cannot be None"
        assert message, "Message cannot be None"

        try:
            request_url = self.url + f"?From={sender}&To={receiver}" \
                          + f"&Content={message}&ClientID={self.client_id}" \
                          + f"&ClientSecret={self.client_secret}" \
                          + f"&RegisteredDelivery=true"
            result = request("GET", request_url)
            return result.json()
        except RequestException:
            raise AppException.OperationError(context="Error sending sms")

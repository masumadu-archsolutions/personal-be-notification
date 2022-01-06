import secrets

from requests import RequestException


class MockResponse:
    def __init__(self, status_code, json):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


class MockSideEffects:

    status_code = 200
    json = None

    def send_sms_response(self, *args, **kwargs):
        return MockResponse(
            status_code=200,
            json={
                "messageId": secrets.token_hex(15),
            },
        )

    def request_exception(self, *args, **kwargs):
        raise RequestException

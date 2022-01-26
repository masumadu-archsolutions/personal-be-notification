from loguru import logger
from pywebpush import WebPushException, webpush

from app.core.exceptions import AppException
from app.core.service_interfaces import PushServiceInterface
from config import Config

VAPID_PRIVATE_KEY = Config.VAPID_PRIVATE_KEY
VAPID_PUBLIC_KEY = Config.VAPID_PUBLIC_KEY
VAPID_CLAIMS = {"sub": "mailto:m@g.com"}


class PushService(PushServiceInterface):
    def send(self, subscription_info, message):
        assert subscription_info, "subscription info cannot be None"
        assert message, "message cannot be None"

        try:
            webpush(
                subscription_info=subscription_info,
                data=message,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS,
            )
            logger.info("push notification sent successful")
        except WebPushException as exc:
            logger.error(
                f"error sending push notification with error message {exc.args}"
            )
            raise AppException.OperationError(context="Error sending push")

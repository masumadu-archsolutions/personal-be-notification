import datetime
import enum
import uuid

from dataclasses import dataclass

from sqlalchemy.sql import func
from app import db


class SMSTypeEnum(enum.Enum):
    otp = "otp"
    password_reset = "password_reset"
    notification = "notification"
    general = "general"
    other = "other"


@dataclass
class SMS(db.Model):
    id: str
    recipient: str
    message_type: str
    message: str
    reference: str
    sms_client: str
    delivered_to_sms_client: bool
    created: datetime.datetime

    __tablename__ = "sms"
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    recipient = db.Column(db.String(15), nullable=False)
    message_type = db.Column(db.Enum(SMSTypeEnum, name="message_type"), nullable=False)
    message = db.Column(db.String())
    reference = db.Column(db.String(60))
    sms_client = db.Column(db.String(60))
    delivered_to_sms_client = db.Column(db.Boolean(), default=False)
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )

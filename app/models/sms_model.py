import enum
import uuid
from sqlalchemy.sql import func
from app import db


class SMSTypeEnum(enum.Enum):
    otp = "otp"
    password_reset = "password_reset"
    notification = "notification"
    general = "general"
    other = "other"


class SMS(db.Model):
    __tablename__ = "sms"
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    recipient = db.Column(db.String(15), nullable=False)
    message_type = db.Column(
        db.Enum(SMSTypeEnum, name="message_type"), nullable=False
    )
    message = db.Column(
        db.String()
    )
    reference = db.Column(db.String(60))
    sms_client = db.Column(db.String(60))
    delivered_to_sms_client = db.Column(db.Boolean(), default=False)
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )

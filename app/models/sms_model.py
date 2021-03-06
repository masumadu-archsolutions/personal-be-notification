import datetime
import uuid
from dataclasses import dataclass

from sqlalchemy.sql import func

from app import db


@dataclass
class SMSModel(db.Model):
    id: str
    recipient: str
    message_type: str
    message_subtype: str
    message_template: str
    message: str
    reference: str
    sms_client: str
    delivered_to_sms_client: bool
    created: datetime.datetime

    __tablename__ = "sms_notification"
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    recipient = db.Column(db.String(15), nullable=False)
    message_type = db.Column(db.String(20), nullable=False)
    message_subtype = db.Column(db.String(20), nullable=False)
    message_template = db.Column(db.String(), nullable=False)
    message = db.Column(db.String(), nullable=False)
    sms_client = db.Column(db.String(60))
    delivered_to_sms_client = db.Column(db.Boolean(), default=False)
    reference = db.Column(db.String(60))
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )

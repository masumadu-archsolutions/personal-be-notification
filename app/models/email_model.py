import enum
import uuid

from sqlalchemy.sql import func

from app import db


class EmailTypeEnum(enum.Enum):
    notification = "notification"
    general = "general"


class EmailModel(db.Model):
    __tablename__ = "email"
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    recipient_email = db.Column(db.String(60))
    message_type = db.Column()
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )

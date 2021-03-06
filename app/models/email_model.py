import uuid

from sqlalchemy.sql import func

from app import db


class EmailModel(db.Model):
    __tablename__ = "email_notification"

    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    recipient = db.Column(db.String(), nullable=False)
    message_type = db.Column(db.String(), nullable=False)
    message_subtype = db.Column(db.String(), nullable=False)
    message_template = db.Column(db.String(), nullable=False)
    email_client = db.Column(db.String())
    delivered_to_email_client = db.Column(db.Boolean(), default=False)
    reference = db.Column(db.String())
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )

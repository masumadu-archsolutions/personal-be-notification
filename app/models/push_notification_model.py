import uuid

from sqlalchemy import Index
from sqlalchemy.sql import func

from app import db


class PushMessageModel(db.Model):
    __tablename__ = "push_messages"

    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    message_type = db.Column(db.String(), nullable=False, index=True)
    message_subtype = db.Column(db.Text(), nullable=False, index=True)
    message_title = db.Column(db.String(), nullable=False)
    message_body = db.Column(db.String(), nullable=False)
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    __table_args__ = (
        Index("push_message_index", "message_type", "message_subtype", unique=True),
    )


class PushSubscriptionModel(db.Model):
    __tablename__ = "push_subscriptions"

    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    endpoint = db.Column(db.String(), nullable=False, unique=True, index=True)
    auth_keys = db.Column(db.Text(), nullable=False)
    subscription_time = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    message_id = db.Column(db.String())
    delivered_to_device = db.Column(db.Boolean(), default=False)
    time_delivered = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

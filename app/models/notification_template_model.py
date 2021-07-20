import uuid
import datetime

from sqlalchemy.sql import func
from dataclasses import dataclass
from app import db


@dataclass
class NotificationTemplate:
    __tablename__ = "notification_template"

    id: str
    type: str
    subtype: str
    created: datetime.datetime
    modified: datetime.datetime

    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    type = db.String()
    subtype = db.String()
    template = db.String()
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    modified = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

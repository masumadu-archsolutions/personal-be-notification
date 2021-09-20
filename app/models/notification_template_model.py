import uuid
import datetime
import json

from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Index
from dataclasses import dataclass
from app import db


@dataclass
class NotificationTemplate(db.Model):
    id: str
    type: str
    subtype: str
    template_keywords: str
    created: datetime.datetime
    modified: datetime.datetime

    __tablename__ = "notification_template"
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    type = db.Column(db.String())
    subtype = db.Column(db.String())
    message = db.Column(db.String())
    template_keywords = db.Column(db.String())
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    modified = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (Index("type_subtype_index", "type", "subtype", unique=True),)

    def __init__(self, type, subtype, message, keywords=None):  # noqa
        self.type = type
        self.subtype = subtype
        self.message = message
        self.template_keywords = json.dumps(keywords)

    @hybrid_property
    def keywords(self):
        return json.loads(self.template_keywords) if self.template_keywords else None

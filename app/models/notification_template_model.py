import datetime
import json
import uuid
from dataclasses import dataclass

from sqlalchemy import Index
from sqlalchemy.sql import func

from app import db


@dataclass
class NotificationTemplateModel(db.Model):
    id: str
    type: str
    subtype: str
    template_file: str
    template_keywords: str
    created: datetime.datetime
    modified: datetime.datetime

    __tablename__ = "notification_template"
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    type = db.Column(db.String(), nullable=False)
    subtype = db.Column(db.String(), nullable=False)
    template_file = db.Column(db.String(), nullable=False)
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

    @property
    def keywords(self):
        return json.loads(self.template_keywords)

    @keywords.setter
    def keywords(self, keywords):
        self.template_keywords = json.dumps(keywords)

from app.definitions.repository import SQLBaseRepository
from app.models import NotificationTemplate


class NotificationTemplateRepository(SQLBaseRepository):
    model = NotificationTemplate

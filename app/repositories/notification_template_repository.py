from app.core.repository import SQLBaseRepository
from app.models import NotificationTemplate


class NotificationTemplateRepository(SQLBaseRepository):
    model = NotificationTemplate

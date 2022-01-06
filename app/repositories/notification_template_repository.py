from app.core.repository import SQLBaseRepository
from app.models import NotificationTemplateModel


class NotificationTemplateRepository(SQLBaseRepository):
    model = NotificationTemplateModel

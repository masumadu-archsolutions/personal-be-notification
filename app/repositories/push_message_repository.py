from app.core.repository import SQLBaseRepository
from app.models import PushMessageModel


class PushMessageRepository(SQLBaseRepository):
    model = PushMessageModel

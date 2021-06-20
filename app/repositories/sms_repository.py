from app.definitions.repository import SQLBaseRepository
from app.models import SMS


class SMSRepository(SQLBaseRepository):
    model = SMS

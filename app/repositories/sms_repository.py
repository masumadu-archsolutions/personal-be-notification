from app.core.repository import SQLBaseRepository
from app.models import SMS


class SmsRepository(SQLBaseRepository):
    model = SMS

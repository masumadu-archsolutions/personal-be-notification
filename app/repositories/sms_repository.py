from app.core.repository import SQLBaseRepository
from app.models import SMSModel


class SmsRepository(SQLBaseRepository):
    model = SMSModel

from app.core.repository import SQLBaseRepository
from app.models import EmailModel


class EmailRepository(SQLBaseRepository):
    model = EmailModel

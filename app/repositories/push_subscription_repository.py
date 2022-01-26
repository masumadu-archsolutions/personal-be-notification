from app.core.repository import SQLBaseRepository
from app.models import PushSubscriptionModel


class PushSubscriptionRepository(SQLBaseRepository):
    model = PushSubscriptionModel

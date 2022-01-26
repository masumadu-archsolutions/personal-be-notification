import enum


class NotificationEnum(enum.Enum):
    sms = {"type": "sms_notification", "subtype": ["otp", "pin_change"]}
    email = {"type": "email_notification", "subtype": ["general"]}
    push = {"type": "push_notification", "subtype": ["general"]}


def get_notification_type():
    notification_type = []
    for notification in NotificationEnum:
        notification_type.append(notification.value.get("type"))
    return notification_type


def get_notification_subtype():
    notification_subtype = set()
    for notification in NotificationEnum:
        for subtype in notification.value.get("subtype"):
            notification_subtype.add(subtype)
    return notification_subtype


def get_subtype(notification_type):
    for notification in NotificationEnum:
        notification_value = notification.value
        if notification_value.get("type") == notification_type:
            return notification_value.get("subtype")

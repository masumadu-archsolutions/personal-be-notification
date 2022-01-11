import enum


class NotificationEnum(enum.Enum):
    sms = {"type": "sms_notification", "subtype": ["otp", "pin_change"]}
    email = {"type": "email_notification", "subtype": ["general"]}
    push = {"type": "push_notification", "subtype": []}


def get_notification_type():
    notification_type = []
    for notification in NotificationEnum:
        notification_type.append(notification.value.get("type"))
    return notification_type


def get_notification_subtype():
    notification_subtype = []
    for notification in NotificationEnum:
        for subtype in notification.value.get("subtype"):
            notification_subtype.append(subtype)
    return notification_subtype


def get_subtype(notification_type):
    for notification in NotificationEnum:
        enum_value = notification.value
        if notification_type and enum_value.get("type") == notification_type:
            return enum_value.get("subtype")

import enum


class NotificationEnum(enum.Enum):
    sms = {"type": "sms_notification", "subtype": ["otp", "pin_change"]}
    email = {"type": "email_notification", "subtype": ["general"]}
    push = {"type": "push_notification", "subtype": []}


def notification_channel():
    channel = []
    for notification in NotificationEnum:
        channel.append(notification.value.get("type"))
    return channel


def channel_subtype():
    notification_subtype = []
    for notification in NotificationEnum:
        for subtype in notification.value.get("subtype"):
            notification_subtype.append(subtype)
    return notification_subtype

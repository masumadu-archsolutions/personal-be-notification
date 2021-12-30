import enum


class SMSTypeEnum(enum.Enum):
    otp = "otp"
    pin_change = "pin_change"


class EmailTypeEnum(enum.Enum):
    notification = "notification"
    general = "general"

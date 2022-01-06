class TemplateTestData:
    @property
    def existing_template(self):
        return {
            "type": "sms_notification",
            "subtype": "otp",
            "message": "[Nova-Gas] Hello, your verification code is \
                        {{ verification_code }}. Do not share this code with anyone. \
                        Thank You",
            "keywords": [
                {
                    "placeholder": "verification_code",
                    "description": "Otp sent to user",
                    "is_sensitive": True,
                }
            ],
        }

    @property
    def new_template(self):
        return {
            "type": "sms_notification",
            "subtype": "pin_change",
            "message": "[Nova-Gas] Hello {{ name }}, your nova account password has been\
                        reset. If you didn't perform this action, please send as a mail\
                        support@nova.com. Thank You!!!",
            "keywords": [
                {
                    "placeholder": "name",
                    "description": "Name of account holder",
                    "is_sensitive": False,
                }
            ],
        }

    @property
    def update_template(self):
        return {
            "type": "email_notification",
            "keywords": [
                {
                    "placeholder": "email",
                    "description": "email of account holder",
                    "is_sensitive": False,
                }
            ],
        }


class SMSTestData:
    @property
    def existing_sms(self):
        return {
            "recipient": "0247049595",
            "message_type": "sms_notification",
            "message": "Hello John, your verification code is 123456",
        }

    @property
    def new_sms(self):
        return {
            "recipient": "0241112223",
            "details": {"verification_code": "123456"},
            "meta": {"type": "sms_notification", "subtype": "otp"},
        }

    @property
    def send_sms(self):
        return {
            "sender": "Quantum",
            "recipient": "0204595050",
            "message": "test message",
        }

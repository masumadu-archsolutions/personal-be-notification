class TemplateFiles:
    @property
    def template_files(self):
        return {
            "sms": "test_sms_notification_otp.txt",
            "email": "test_email_notification_general.html",
        }


class TemplateTestData(TemplateFiles):
    @property
    def existing_template(self):
        sms_template = {
            "type": "sms_notification",
            "subtype": "otp",
            "template_file": self.template_files.get("sms"),
            "keywords": [
                {
                    "placeholder": "verification_code",
                    "description": "Otp sent to user",
                    "is_sensitive": True,
                },
            ],
        }
        email_template = {
            "type": "email_notification",
            "subtype": "general",
            "template_file": self.template_files.get("email"),
            "keywords": [
                {
                    "placeholder": "Name",
                    "description": "Name of user",
                    "is_sensitive": True,
                },
            ],
        }
        return [sms_template, email_template]

    @property
    def new_template(self):
        return {
            "type": "sms_notification",
            "subtype": "pin_change",
            "template_file": "new_template_file",
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
            "keywords": [
                {
                    "placeholder": "username",
                    "description": "username of account holder",
                    "is_sensitive": False,
                }
            ],
        }


class SMSTestData(TemplateFiles):
    @property
    def existing_sms(self):
        return {
            "recipient": "0247049595",
            "message_type": "sms_notification",
            "message_subtype": "otp",
            "message_template": self.template_files.get("sms"),
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


class EmailTestData(TemplateFiles):
    @property
    def existing_email(self):
        return {
            "recipient": "test@example.com",
            "message_type": "sms_notification",
            "message_subtype": "general",
            "message_template": self.template_files.get("email"),
        }

    @property
    def new_email(self):
        return {
            "recipient": "test@example.com",
            "details": {"name": "send_email_view"},
            "meta": {"type": "email_notification", "subtype": "general"},
        }

    @property
    def send_email(self):
        return {
            "recipient": "test_example@gmail.com",
            "email_body": "<h1>email body </h1>",
        }

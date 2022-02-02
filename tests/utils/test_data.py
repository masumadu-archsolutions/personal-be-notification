import uuid


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
    def sms_request_data(self):
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
    def email_request_data(self):
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


class PushMessageTestData:
    @property
    def existing_message(self):
        return {
            "message_type": "push_notification",
            "message_subtype": "transaction_alert",
            "message_title": "message title",
            "message_body": "push message body",
        }

    @property
    def new_message(self):
        return {
            "message_type": "push_notification",
            "message_subtype": "general",
            "message_title": "message title",
            "message_body": "push message body",
        }

    @property
    def update_message(self):
        return {"message_body": "updated message body"}


class PushSubscriptionTestData(PushMessageTestData):
    @property
    def existing_subscription(self):
        return {
            "endpoint": "https://fcm.googleapis.com/fcm/send/ecLd9nk2p2g:APA91bE5XkgCu0vkZU7mLXti3WjU-LhDOAY3-G7ZzI0QOVnw-bPJo7ZlzWWzQzyFoH2AiXiFkcemjL3S0UjsVr3yJVNW3XbeIfhfWlKuOhx04LjObGUsKejWQxxFnpWg5TBHdxCiBRXR",  # noqa
            "auth_keys": '{"p256dh":"BJfAdP6roL7dH9a6yR2diiK6FKLIzG23fSbi9PwEsZjgErrOQ92ecv0GkFaTMq6AVGptS2D24pF4MHysZfi2STg","auth":"zQGpi3vX2zWSt9QjbSmO_A"}',  # noqa
        }

    @property
    def new_subscription(self):
        return {
            "endpoint": "https://fcm.googleapis.com/fcm/send/frN610kGF1E:APA91bHKXS6PaEx_cVYoU52c9jol0-JJd6vlh47UjfLXCL0P2Cds349DEe6hVsE5nz6Ny2XG_zRa28jCWvhafhcovHEJRFWY_nj8BInPfKePzufv8mbYNeh-jVtzOHBorhxZ0FF-8aiR",  # noqa
            "auth_keys": '{"p256dh":"BMGlN0vMuU_oQjoOPxEBWS_jJ1-hdlHN98AE3cawyAlBYBHkynEAsnKpiYgi4Ee3g07W7cVFlXAkYdt0V6p_Zlg","auth":"-YioKWEX3vxxcCGFH7Qr8Q"}',  # noqa
        }

    @property
    def send_push_request(self):
        return {
            "endpoint": self.existing_subscription.get("endpoint"),
            "metadata": {
                "message_type": self.existing_message.get("message_type"),
                "message_subtype": self.existing_message.get("message_subtype"),
            },
        }

    @property
    def send_push_request_exc(self):
        return {
            "endpoint": self.new_subscription.get("endpoint"),
            "metadata": {
                "message_type": self.new_message.get("message_type"),
                "message_subtype": self.existing_message.get("message_subtype"),
            },
        }

    @property
    def send_push(self):
        return {
            "subscription_info": {
                "endpoint": self.existing_subscription.get("endpoint"),
                "keys": self.existing_subscription.get("auth_keys"),
            },
            "message": {
                "message_id": str(uuid.uuid4()),
                "message_title": "push title",
                "message_body": "push message",
            },
            "endpoint_id": str(uuid.uuid4()),
        }

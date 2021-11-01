import os
from flask_testing import TestCase
from app import create_app, db
from app.controllers import SmsController
from app.repositories import NotificationTemplateRepository, SmsRepository
from app.services import SmsService
from config import Config


class BaseTestCase(TestCase):
    keywords = [
        {"description": "The username", "is_sensitive": True, "placeholder": "username"}
    ]

    message = "Hello {{username}}, have a great day"
    message_type = "sms_notification"
    subtype = "daily_greeting"

    data = {
        "keywords": keywords,
        "message": message,
        "type": message_type,
        "subtype": subtype,
    }

    def create_app(self):
        app = create_app("config.TestingConfig")
        self.template_repository = NotificationTemplateRepository()
        self.sms_repository = SmsRepository()
        self.sms_controller = SmsController(
            self.sms_repository, self.template_repository, SmsService()
        )
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa: E501
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.app_name = Config.APP_NAME
        return app

    @property
    def template(self):
        return self.template_repository.create(self.data)

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

        file = f"{Config.SQL_DB_NAME}.sqlite3"
        os.remove(file)

    def required_roles_side_effect(  # noqa
        self, token, key, algorithms, audience, issuer
    ):
        return {
            "realm_access": {
                "roles": [
                    f"{Config.APP_NAME}_create_employee",
                    f"{Config.APP_NAME}_update_employee",
                    f"{Config.APP_NAME}_show_employee",
                    f"{Config.APP_NAME}_delete_employee",
                    f"{Config.APP_NAME}_create_distributor",
                    f"{Config.APP_NAME}_get_distributor",
                    f"{Config.APP_NAME}_get_all_distributors",
                    f"{Config.APP_NAME}_delete_distributor",
                    f"{Config.APP_NAME}_update_distributor",
                ]
            },
        }

    def no_role_side_effect(self, token, key, algorithms, audience, issuer):  # noqa
        return {
            "realm_access": {"roles": []},
        }

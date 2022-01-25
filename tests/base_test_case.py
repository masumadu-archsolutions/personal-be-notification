import os

from flask_testing import TestCase

import config
from app import APP_ROOT, create_app, db, init_celery
from app.controllers import (
    EmailController,
    NotificationTemplateController,
    SmsController,
)
from app.models import EmailModel, NotificationTemplateModel, SMSModel
from app.repositories import (
    EmailRepository,
    NotificationTemplateRepository,
    SmsRepository,
)
from app.services import EmailService, SmsService
from tests.utils import EmailTestData, MockSideEffects, SMSTestData, TemplateTestData


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        self.setup_patches()
        self.instantiate_classes()
        self.setup_template_files()
        return app

    def init_celery(self):
        return init_celery(self.create_app())

    def instantiate_classes(self):
        self.template_repository = NotificationTemplateRepository()
        self.template_controller = NotificationTemplateController(
            self.template_repository
        )
        self.sms_repository = SmsRepository()
        self.email_repository = EmailRepository()
        self.sms_service = SmsService()
        self.email_service = EmailService()
        self.sms_controller = SmsController(
            self.sms_repository, self.template_repository, self.sms_service
        )
        self.email_controller = EmailController(
            self.email_repository, self.template_repository, self.email_service
        )
        self.template_test_data = TemplateTestData()
        self.sms_test_data = SMSTestData()
        self.email_test_data = EmailTestData()
        self.side_effect = MockSideEffects()

    def setup_patches(self):
        pass

    def setup_template_files(self):
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        templates_directory = f"{parent_directory}/app/templates"
        template_files = self.template_test_data.template_files
        for key in template_files:
            file_directory = f"{templates_directory}/{key}"
            with open(f"{file_directory}/{template_files.get(key)}", "w") as test_file:
                test_file.write("sample template file")
        self.templates_directory = templates_directory

    def remove_template_files(self):
        template_files = self.template_test_data.template_files
        for key in template_files:
            os.remove(
                os.path.join(
                    f"{self.templates_directory}/{key}", template_files.get(key)
                )
            )

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        self.sms_template_test_model = NotificationTemplateModel(
            **self.template_test_data.existing_template[0],
        )
        self.email_template_test_model = NotificationTemplateModel(
            **self.template_test_data.existing_template[1],
        )
        self.sms_model = SMSModel(**self.sms_test_data.existing_sms)
        self.email_model = EmailModel(**self.email_test_data.existing_email)
        db.session.add(self.sms_template_test_model)
        db.session.add(self.email_template_test_model)
        db.session.add(self.sms_model)
        db.session.add(self.email_model)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

        file = f"{config.Config.SQL_DB_NAME}.sqlite3"
        file_path = os.path.join(APP_ROOT, file)
        os.remove(file_path)
        self.remove_template_files()

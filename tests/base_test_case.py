import os

from flask_testing import TestCase

import config
from app import APP_ROOT, create_app, db, init_celery
from app.controllers import NotificationTemplateController, SmsController
from app.models import NotificationTemplateModel, SMSModel
from app.repositories import NotificationTemplateRepository, SmsRepository
from app.services import SmsService
from tests.utils import MockSideEffects, SMSTestData, TemplateTestData


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        self.setup_patches()
        self.instantiate_classes()
        return app

    def init_celery(self):
        return init_celery(self.create_app())

    def instantiate_classes(self):
        self.template_repository = NotificationTemplateRepository()
        self.template_controller = NotificationTemplateController(
            self.template_repository
        )
        self.sms_repository = SmsRepository()
        self.sms_service = SmsService()
        self.sms_controller = SmsController(
            self.sms_repository, self.template_repository, self.sms_service
        )
        self.template_test_data = TemplateTestData()
        self.sms_test_data = SMSTestData()
        self.side_effect = MockSideEffects()

    def setup_patches(self):
        pass

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        self.template_test_model = NotificationTemplateModel(
            **self.template_test_data.existing_template
        )
        self.sms_model = SMSModel(**self.sms_test_data.existing_sms)
        db.session.add(self.template_test_model)
        db.session.add(self.sms_model)
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

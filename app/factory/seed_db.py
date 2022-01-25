from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from app.core.factory import Seeder
from app.enums import get_notification_subtype, get_notification_type
from app.models import EmailModel, NotificationTemplateModel, SMSModel


def generate_random_keywords(placeholder, description, is_sensitive):
    keywords = (
        [
            {
                "placeholder": placeholder,
                "description": description,
                "is_sensitive": is_sensitive,
            }
        ],
    )
    return keywords


class SeedNotificationTemplateModel(Seeder):
    @classmethod
    def run(cls):
        template = NotificationTemplateModel(
            type=cls.fake.random_element(get_notification_type()),
            subtype=cls.fake.random_element(get_notification_subtype()),
            template_file=cls.fake.text(),
            keywords=generate_random_keywords(
                placeholder=cls.fake.word(),
                description=cls.fake.sentence(),
                is_sensitive=cls.fake.boolean(),
            ),
        )
        cls.db.session.add(template)
        try:
            cls.db.session.commit()
        except SQLAlchemyError as e:
            logger.error(e.args)
            cls.db.session.rollback()


class SeedSMSModel(Seeder):
    @classmethod
    def run(cls):
        sms = SMSModel(
            recipient=cls.fake.random_number(digits=10, fix_len=True),
            message_type=cls.fake.random_element(elements=get_notification_type()),
            message_subtype=cls.fake.random_element(elements=get_notification_subtype()),
            message_template=cls.fake.word(),
            message=cls.fake.text(),
            reference=cls.fake.random_number(digits=15, fix_len=True),
            sms_client=cls.fake.word(),
            delivered_to_sms_client=cls.fake.boolean(),
        )
        cls.db.session.add(sms)
        try:
            cls.db.session.commit()
        except SQLAlchemyError as e:
            logger.error(e.args)
            cls.db.session.rollback()


class SeedEmailModel(Seeder):
    @classmethod
    def run(cls):
        email = EmailModel(
            recipient=cls.fake.word(),
            message_type=cls.fake.word(),
            message_subtype=cls.fake.word(),
            message_template=cls.fake.word(),
            reference=cls.fake.random_number(digits=15, fix_len=True),
            email_client=cls.fake.word(),
            delivered_to_email_client=cls.fake.boolean(),
        )
        cls.db.session.add(email)
        try:
            cls.db.session.commit()
        except SQLAlchemyError as e:
            logger.error(e.args)
            cls.db.session.rollback()

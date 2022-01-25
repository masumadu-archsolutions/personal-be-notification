import os
import sys

from dotenv import load_dotenv

from app import dotenv_path

load_dotenv(dotenv_path)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Set Flask configuration vars from .env file."""

    SERVICE_NAME = "Notification Service"
    FLASK_ENV = os.getenv("FLASK_ENV")
    DB_ENGINE = os.getenv("DB_ENGINE", default="POSTGRES")

    # SQL database
    SQL_DB_USER = os.getenv("DB_USER")
    SQL_DB_HOST = ""
    SQL_DB_NAME = os.getenv("DB_NAME")
    SQL_DB_PASSWORD = os.getenv("DB_PASSWORD")
    SQL_DB_PORT = os.getenv("DB_PORT", default=5432)

    # MONGO database
    MONGODB_DB = os.getenv("DB_NAME")
    MONGODB_PORT = int(os.getenv("DB_PORT", default=27017))
    MONGODB_USERNAME = os.getenv("DB_USER")
    MONGODB_PASSWORD = os.getenv("DB_PASSWORD")
    MONGODB_CONNECT = False

    # REDIS
    REDIS_SERVER = os.getenv("REDIS_SERVER", default="localhost")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # General
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="SECRETKEY")
    FLASK_RUN_PORT = 6000
    TESTING = False
    LOGFILE = "log.log"
    APP_NAME = "notification"

    # SMS
    SMS_CLIENT_ID = os.getenv("SMS_CLIENT_ID")
    SMS_CLIENT_SECRET = os.getenv("SMS_CLIENT_SECRET")

    # EMAIL
    EMAIL_CLIENT_API = os.getenv("EMAIL_PROVIDER_API")

    # TLS MAIL CONFIGURATION
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", default=25))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", default=True)
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", default=False)
    MAIL_DEFAULT_SENDER = os.getenv("ADMIN_EMAIL_ADDRESS")

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return "postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}".format(
            user=self.SQL_DB_USER,
            pw=self.SQL_DB_PASSWORD,
            url=self.SQL_DB_HOST,
            port=self.SQL_DB_PORT,
            db=self.SQL_DB_NAME,
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @property
    def CELERY(self):
        return {
            "broker_url": f"redis://{self.REDIS_SERVER}:{self.REDIS_PORT}",
            "result_backend": f"redis://{self.REDIS_SERVER}:{self.REDIS_PORT}",
        }


class DevelopmentConfig(Config):

    DEBUG = True
    DEVELOPMENT = True
    SQL_DB_HOST = os.getenv("DEV_DB_HOST")
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    SQL_DB_HOST = os.getenv("DB_HOST")
    LOG_BACKTRACE = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return (
            f"sqlite:///{os.path.join('..', self.SQL_DB_NAME)}"
            f".sqlite3?check_same_thread=False"
        )

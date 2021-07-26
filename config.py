import os
import sys
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Set Flask configuration vars from .env file."""

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
    REDIS_SERVER = os.getenv("REDIS_SERVER")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    # General
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = "SECRET"
    FLASK_RUN_PORT = 6000
    TESTING = False
    LOGFILE = "log.log"

    @property
    def CELERY_BROKER_URL(self):
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_SERVER}"

    @property
    def CELERY_RESULT_BACKEND(self):
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_SERVER}"

    # SMS
    SMS_CLIENT_ID = os.getenv("SMS_CLIENT_ID")
    SMS_CLIENT_SECRET = os.getenv("SMS_CLIENT_SECRET")

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

    CELERY = {
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379",
    }


class DevelopmentConfig(Config):
    @property
    def CELERY_BROKER_URL(self):
        return (f"redis://{self.REDIS_SERVER}:6379",)

    @property
    def CELERY_RESULT_BACKEND(self):
        return f"redis://{self.REDIS_SERVER}:6379"

    DEBUG = True
    DEVELOPMENT = True
    DB_SERVER = os.getenv("DEV_DB_SERVER")
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    DB_SERVER = os.getenv("DB_SERVER")
    LOG_BACKTRACE = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    DB_NAME = "test"
    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, DB_NAME) + ".sqlite3"

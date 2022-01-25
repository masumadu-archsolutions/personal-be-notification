from celery import Celery
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.utils import GUID

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()
db.__setattr__("GUID", GUID)


celery = Celery()

import json
import os
import sys

import pinject
from dotenv import load_dotenv
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from loguru import logger

# Add "app" root to PYTHONPATH so we can import from app i.e. from app import create_app.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # noqa

from app import APP_ROOT, create_app  # noqa: E402

# load .env file into system
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

KAFKA_SUBSCRIPTIONS = os.getenv("KAFKA_SUBSCRIPTIONS", default="SMS_NOTIFICATION")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", default="localhost:9092")
KAFKA_CONSUMER_GROUP_ID = os.getenv(
    "KAFKA_CONSUMER_GROUP_ID", default="NOTIFICATION_CONSUMER_GROUP"
)
subscriptions = KAFKA_SUBSCRIPTIONS.split("|")
bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS.split("|")

if __name__ == "__main__":
    logger.info("CONNECTING TO SERVER")
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="earliest",
            group_id=KAFKA_CONSUMER_GROUP_ID,
        )
    except KafkaError as exc:
        logger.error(f"Failed to consume message on Kafka broker with error {exc}")
    else:
        consumer.subscribe(subscriptions)
        logger.info("AWAITING MESSAGES\n")

        app = create_app()
        app_ctx = app.app_context()
        app_ctx.push()

        # Application context should be registered before importing from app
        from app.controllers import EmailController, SmsController
        from app.repositories import (
            EmailRepository,
            NotificationTemplateRepository,
            SmsRepository,
        )
        from app.services import EmailService, SmsService

        for msg in consumer:
            data = json.loads(msg.value)
            logger.info(f"originating service: {data.get('service_name')}")
            logger.info(f"topic consuming: {msg.topic}")
            if msg.topic == "SMS_NOTIFICATION":
                obj_graph = pinject.new_object_graph(
                    modules=None,
                    classes=[
                        SmsController,
                        SmsRepository,
                        SmsService,
                        NotificationTemplateRepository,
                    ],
                )
                sms_controller = obj_graph.provide(SmsController)
                sms_controller.send_message(data)
            elif msg.topic == "EMAIL_NOTIFICATION":
                obj_graph = pinject.new_object_graph(
                    modules=None,
                    classes=[
                        EmailController,
                        EmailRepository,
                        EmailService,
                        NotificationTemplateRepository,
                    ],
                )
                email_controller = obj_graph.provide(EmailController)
                email_controller.send_mail(data)
            logger.info("message status: successfully consumed\n")

import json
import os
import sys

import pinject
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from loguru import logger

# Add "app" root to PYTHONPATH so we can import from app i.e. from app import create_app.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # noqa

from app import create_app  # noqa: E402

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
        logger.info("AWAITING MESSAGES")

        app = create_app()
        app_ctx = app.app_context()
        app_ctx.push()

        # Application context should be registered before importing from app
        from app.controllers import SmsController
        from app.repositories import NotificationTemplateRepository, SmsRepository
        from app.services import SmsService

        for msg in consumer:
            logger.info("message received")
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
                data = json.loads(msg.value)
                sms_controller.send_message(data)
            logger.info("message successfully consumed\n")

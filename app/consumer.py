import json
import os
from kafka import KafkaConsumer
import pinject

from app import create_app


KAFKA_SUBSCRIPTIONS = \
    os.getenv("KAFKA_SUBSCRIPTIONS", default="SMS_NOTIFICATION")
KAFKA_BOOTSTRAP_SERVERS = \
    os.getenv("KAFKA_BOOTSTRAP_SERVERS", default="localhost:9092")
KAFKA_CONSUMER_GROUP_ID = \
    os.getenv("KAFKA_CONSUMER_GROUP_ID", default="NOTIFICATION_CONSUMER_GROUP")
subscriptions = KAFKA_SUBSCRIPTIONS.split("|")
bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS.split("|")

if __name__ == "__main__":
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        group_id=KAFKA_CONSUMER_GROUP_ID,
    )

    consumer.subscribe(subscriptions)
    print("starting consumer...")

    app = create_app()
    app_ctx = app.app_context()
    app_ctx.push()

    # Application context should be registered before importing from app
    from app.controllers import SmsController
    from app.repositories import SmsRepository
    from app.services import SmsService

    for msg in consumer:

        if msg.topic == "SMS_NOTIFICATION":
            obj_graph = pinject.new_object_graph(
                modules=None, classes=
                [SmsController, SmsRepository, SmsService]
            )
            sms_controller = obj_graph.provide(SmsController)

            data = json.loads(msg.value)
            print(data)
            sms_controller.send_token(data)

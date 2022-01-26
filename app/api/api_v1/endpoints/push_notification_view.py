import pinject
from flask import Blueprint, request

from app.controllers import PushSubscriptionController
from app.core.service_result import handle_result
from app.repositories import PushMessageRepository, PushSubscriptionRepository
from app.schema import (
    CreateMessageSchema,
    CreateSubscriptionSchema,
    PushMessageSchema,
    SendMessageSchema,
    SubscriptionSchema,
    UpdateMessageSchema,
)
from app.services import PushService
from app.utils import validator

push_subscription = Blueprint("push", __name__)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        PushSubscriptionController,
        PushSubscriptionRepository,
        PushService,
        PushMessageRepository,
    ],
)

push_controller = obj_graph.provide(PushSubscriptionController)


@push_subscription.route("/message", methods=["POST"])
@validator(schema=CreateMessageSchema)
def create_message():
    """
    ---
    post:
      description: create a push notification message
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateMessageSchema
      responses:
        '201':
          description: call successful
          content:
            application/json:
              schema: PushMessageSchema
      tags:
          - Push
    """
    data = request.json
    result = push_controller.create_message(data)
    return handle_result(result, schema=PushMessageSchema)


@push_subscription.route("/message", methods=["GET"])
def get_all_messages():
    """
    ---
    get:
      description: get all push notification messages
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: PushMessageSchema
      tags:
          - Push
    """
    result = push_controller.show_all_messages()
    return handle_result(result, schema=PushMessageSchema, many=True)


@push_subscription.route("/message/<message_id>", methods=["GET"])
def get_message(message_id):
    """
    ---
    get:
      description: get a push notification message
      parameters:
        - in: path
          name: message_id
          required: true
          schema:
            type: string
          description: The push message ID
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: PushMessageSchema
      tags:
          - Push
    """
    result = push_controller.show_message(message_id)
    return handle_result(result, schema=PushMessageSchema)


@push_subscription.route("/message/<message_id>", methods=["PATCH"])
@validator(schema=UpdateMessageSchema)
def update_message(message_id):
    """
    ---
    patch:
      description: update a push notification message
      parameters:
        - in: path
          name: message_id
          required: true
          schema:
            type: string
          description: The push message ID
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateMessageSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: PushMessageSchema
      tags:
          - Push
    """
    data = request.json
    result = push_controller.update_message(message_id, data)
    return handle_result(result, schema=PushMessageSchema)


@push_subscription.route("/message/<message_id>", methods=["DELETE"])
def delete_message(message_id):
    """
    ---
    delete:
      description: delete a push notification message
      parameters:
        - in: path
          name: message_id
          required: true
          schema:
            type: string
          description: The push message ID
      responses:
        '204':
          description: returns a nil
      tags:
          - Push
    """
    result = push_controller.delete_message(message_id)
    return handle_result(result)


@push_subscription.route("/subscription", methods=["POST"])
@validator(schema=CreateSubscriptionSchema)
def subscribe():
    """
    ---
    post:
      description: subscribes a user to push notification service
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateSubscriptionSchema
      responses:
        '201':
          description: call successful
          content:
            application/json:
              schema: SubscriptionSchema
      tags:
          - Push
    """
    data = request.json
    result = push_controller.subscribe_user(data)
    return handle_result(result, schema=SubscriptionSchema)


@push_subscription.route("/subscription", methods=["GET"])
def get_all_subscriptions():
    """
    ---
    get:
      description: returns all push subscriptions
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: SubscriptionSchema
      tags:
          - Push
    """
    result = push_controller.show_all_subscriptions()
    return handle_result(result, schema=SubscriptionSchema, many=True)


@push_subscription.route("/subscription/send-message", methods=["POST"])
@validator(schema=SendMessageSchema)
def send_message():
    """
    ---
    post:
      description: send a push notification
      requestBody:
        required: true
        content:
          application/json:
            schema: SendMessageSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema:
                schema:
                type: object
                properties:
                  status:
                    type: string
                    example: successful
        '500':
          description: call unsuccessful
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: unsuccessful
      tags:
          - Push
    """
    data = request.json
    result = push_controller.send_push(data)
    return handle_result(result)


@push_subscription.route("/subscription/server-id", methods=["GET"])
def send_server_id():
    """
    ---
    get:
      description: send server id
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  public_key:
                    type: string
                    example: BEqJ0KCYmkf_0bJhGpQ24SApI_MQumWRkNAkU0NvShmBqfgxpDLmfNDgVmF
      tags:
          - Push
    """
    result = push_controller.server_id()
    return handle_result(result)

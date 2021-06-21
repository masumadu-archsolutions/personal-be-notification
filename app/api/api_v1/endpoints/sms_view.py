import pinject
from flask import Blueprint

from app.controllers import SmsController
from app.definitions.service_result import handle_result
from app.repositories import SmsRepository
from app.schema import SMSSchema
from app.services import SmsService

sms = Blueprint("sms", __name__)

obj_graph = pinject.new_object_graph(
    modules=None, classes=[SmsController, SmsRepository, SmsService]
)

sms_controller = obj_graph.provide(SmsController)


@sms.route("/")
def get_all_sms():
    """
    ---
    get:
      description: returns all sms
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: SMS
      tags:
          - SMS
    """
    result = sms_controller.index()
    return handle_result(result, schema=SMSSchema, many=True)


@sms.route("/<string:sms_id>")
def get_sms(sms_id):
    """
    ---
    get:
      description: returns a product with id specified in path
      parameters:
        - in: path
          name: sms_id   # Note the name is the same as in the path
          required: true
          schema:
            type: string
          description: The sms ID
      responses:
        '200':
          description: returns an sms
          content:
            application/json:
              schema: SMS
      tags:
          - SMS
    """

    result = sms_controller.show(sms_id)
    return handle_result(result, schema=SMSSchema)


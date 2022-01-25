import pinject
from flask import Blueprint

from app.controllers import EmailController
from app.core.service_result import handle_result
from app.repositories import EmailRepository, NotificationTemplateRepository
from app.schema import EmailSchema
from app.services import EmailService

email = Blueprint("email", __name__)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        EmailController,
        NotificationTemplateRepository,
        EmailRepository,
        EmailService,
    ],
)

email_controller = obj_graph.provide(EmailController)


@email.route("/")
def get_all_email():
    """
    ---
    get:
      description: returns all email
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: Email
      tags:
          - Email
    """
    result = email_controller.index()
    return handle_result(result, schema=EmailSchema, many=True)


@email.route("/<string:email_id>")
def get_email(email_id):
    """
    ---
    get:
      description: returns a email with id specified in path
      parameters:
        - in: path
          name: email_id
          required: true
          schema:
            type: string
          description: The email ID
      responses:
        '200':
          description: returns an email
          content:
            application/json:
              schema: Email
      tags:
          - Email
    """

    result = email_controller.show(email_id)
    return handle_result(result, schema=EmailSchema)


@email.route("/send-mail")
def send_email():
    """
    ---
    get:
      description: sends a mail
      responses:
        '200':
          description: returns an email
          content:
            application/json:
              schema: Email
      tags:
          - Email
    """
    data = {
        "recipient": "michaelasumadu1@gmail.com",
        "details": {"name": "send_email_view"},
        "meta": {"type": "email_notification", "subtype": "general"},
    }

    email_controller.send_mail(data)
    return "sent"

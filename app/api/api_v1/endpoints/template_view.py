import pinject
from flask import Blueprint, request

from app.controllers import TemplateController
from app.definitions.service_result import handle_result
from app.repositories import NotificationTemplateRepository
from app.schema import TemplateSchema, TemplateCreateSchema, TemplateUpdateSchema
from app.utils import validator, auth_required

template = Blueprint("template", __name__)

obj_graph = pinject.new_object_graph(
    modules=None, classes=[TemplateController, NotificationTemplateRepository]
)

template_controller = obj_graph.provide(TemplateController)


@template.route("/", methods=["POST"])
@validator(schema=TemplateCreateSchema)
# @auth_required()
def create_template():
    """
    ---
    post:
      description: creates a new template
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema: TemplateCreateSchema
      responses:
        '201':
          description: returns a template
          content:
            application/json:
              schema: TemplateSchema
      tags:
          - Template
    """
    data = request.json
    result = template_controller.create(data)
    return handle_result(result, schema=TemplateSchema)


@template.route("/", methods=["GET"])
# @auth_required()
def get_all_templates():
    """
    ---
    get:
      description: returns all templates
      security:
        - bearerAuth: []
      responses:
        '200':
          description: returns a customer
          content:
            application/json:
              schema:
                type: array
                items: TemplateSchema
      tags:
          - Template
    """
    result = template_controller.index()
    return handle_result(result, schema=TemplateSchema, many=True)


@template.route("/<string:template_id>")
@auth_required()
def get_template(template_id):
    """
    ---
    get:
      description: returns a template with id specified in path
      parameters:
        - in: path
          name: template_id   # Note the name is the same as in the path
          required: true
          schema:
            type: string
          description: The template ID
      responses:
        '200':
          description: returns a template
          content:
            application/json:
              schema: TemplateSchema
      tags:
          - Template
    """
    result = template_controller.show(template_id)
    return handle_result(result, schema=TemplateSchema)


@template.route("/<string:template_id>", methods=["PATCH"])
@validator(schema=TemplateUpdateSchema)
@auth_required()
def update_template(template_id):
    """
    ---
    patch:
      description: updates a template with id specified in path
      parameters:
        - in: path
          name: template_id   # Note the name is the same as in the path
          required: true
          schema:
            type: string
          description: The template ID
      requestBody:
        required: true
        content:
            application/json:
                schema: TemplateUpdateSchema
      security:
        - bearerAuth: []
      responses:
        '200':
          description: returns a template
          content:
            application/json:
              schema: TemplateSchema
      tags:
          - Template
    """
    data = request.json
    result = template_controller.update(template_id, data)
    return handle_result(result, schema=TemplateSchema)


@template.route("/<string:template_id>", methods=["DELETE"])
@auth_required()
def delete_template(template_id):
    """
    ---
    delete:
      description: deletes a template with id specified in path
      parameters:
        - in: path
          name: template_id
          required: true
          schema:
            type: string
          description: The template ID
      security:
        - bearerAuth: []
      responses:
        '200':
          description: returns nothing
      tags:
          - Template
    """
    result = template_controller.delete(template_id)
    return handle_result(result)

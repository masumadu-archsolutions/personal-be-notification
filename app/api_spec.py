"""OpenAPI v3 Specification"""

# apispec via OpenAPI
import json
import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from app.schema import TemplateCreateSchema, TemplateSchema, TemplateUpdateSchema

# get swagger.json file path
swagger_json_path = os.path.dirname(__file__) + "/static/swagger.json"

# load swagger.json file
with open(swagger_json_path) as apispec_info:
    spec_info = json.load(apispec_info).get("info")

# Create an APISpec
spec = APISpec(
    title=spec_info.get("title"),
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    info=spec_info,
)

# Security
api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
bearer_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("ApiKeyAuth", api_key_scheme)
spec.components.security_scheme("bearerAuth", bearer_scheme)

spec.components.schema("TemplateSchema", schema=TemplateSchema)
spec.components.schema("TemplateCreateSchema", schema=TemplateCreateSchema)
spec.components.schema("TemplateUpdateSchema", schema=TemplateUpdateSchema)


# add swagger tags that are used for endpoint annotation
tags = [
    {"name": "Template", "description": "For user authentication."},
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)

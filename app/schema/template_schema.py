from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.enums import get_notification_subtype, get_notification_type, get_subtype


class KeywordSchema(Schema):
    placeholder = fields.String(
        required=True,
        validate=validate.Regexp(
            r"^(\d|\w)+$", error="Should contain no spaces or special keywords"
        ),
        error_messages={"invalid": "Should contain no spaces or special keywords"},
    )
    description = fields.String(required=True)
    is_sensitive = fields.Boolean(default=False)


class TemplateSchema(Schema):
    id = fields.UUID(required=True)
    type = fields.String(required=True, validate=validate.OneOf(get_notification_type()))
    subtype = fields.String(
        required=True,
        validate=validate.OneOf(get_notification_subtype()),
    )
    message = fields.String(required=True)
    keywords = fields.Nested(KeywordSchema(many=True))
    created = fields.DateTime(required=True)
    modified = fields.DateTime(required=True)

    @validates_schema
    def validate_subtype(self, field, **kwargs):
        subtype = field.get("subtype")
        if subtype and subtype not in get_subtype(field.get("type")):
            raise ValidationError(f"subtype must be one of {get_subtype(field['type'])}")

    class Meta:
        fields = [
            "id",
            "type",
            "subtype",
            "message",
            "keywords",
            "created",
            "modified",
        ]
        ordered = True


class TemplateCreateSchema(TemplateSchema):
    class Meta:
        fields = [
            "type",
            "subtype",
            "message",
            "keywords",
        ]


class TemplateUpdateSchema(TemplateSchema):
    type = fields.String(
        required=True,
        validate=validate.OneOf(get_notification_type()),
    )
    subtype = fields.String(validate=validate.OneOf(get_notification_subtype()))
    message = fields.String()
    keywords = fields.Nested(KeywordSchema(many=True))

    class Meta:
        fields = [
            "type",
            "subtype",
            "message",
            "keywords",
        ]

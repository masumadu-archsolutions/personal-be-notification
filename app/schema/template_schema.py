from marshmallow import (
    Schema,
    ValidationError,
    fields,
    pre_load,
    validate,
    validates_schema,
)

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
    id = fields.UUID()
    type = fields.String()
    subtype = fields.String()
    keywords = fields.Nested(KeywordSchema(many=True))
    template_file = fields.String()
    created = fields.DateTime()
    modified = fields.DateTime()

    @validates_schema
    def validate_subtype(self, field, **kwargs):
        message_subtype = field.get("subtype")
        subtype = get_subtype(field.get("type"))
        if message_subtype and message_subtype not in subtype:
            raise ValidationError(f"subtype must be one of {subtype}")

    class Meta:
        fields = [
            "id",
            "type",
            "subtype",
            "template_file",
            "keywords",
            "created",
            "modified",
        ]
        ordered = True


class TemplateCreateSchema(TemplateSchema):
    id = fields.UUID(required=True)
    type = fields.String(required=True, validate=validate.OneOf(get_notification_type()))
    subtype = fields.String(
        required=True,
        validate=validate.OneOf(get_notification_subtype()),
    )
    keywords = fields.Nested(KeywordSchema(many=True))
    template_file = fields.String(required=True)
    created = fields.DateTime(required=True)
    modified = fields.DateTime(required=True)

    class Meta:
        fields = [
            "type",
            "subtype",
            "template_file",
            "keywords",
        ]


class TemplateUpdateSchema(TemplateSchema):
    type = fields.String(
        validate=validate.OneOf(get_notification_type()),
    )
    subtype = fields.String(validate=validate.OneOf(get_notification_subtype()))
    template_file = fields.String()
    keywords = fields.Nested(KeywordSchema(many=True))

    class Meta:
        fields = [
            "type",
            "subtype",
            "template_file",
            "keywords",
        ]

    @pre_load
    def validate_enum(self, field, **kwargs):
        message_type = field.get("type")
        message_subtype = field.get("subtype")
        if message_type and not message_subtype or message_subtype and not message_type:
            raise ValidationError("subtype and type required")
        return field

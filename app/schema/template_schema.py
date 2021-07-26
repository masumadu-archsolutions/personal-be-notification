from marshmallow import Schema, fields, validate


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
    type = fields.String(
        required=True,
        validate=validate.OneOf(
            ["sms_notification", "email_notification", "push_notification"]
        ),
    )
    subtype = fields.String(required=True)
    message = fields.String(required=True)
    keywords = fields.Nested(KeywordSchema(many=True))
    created = fields.DateTime(required=True)
    modified = fields.DateTime(required=True)

    class Meta:
        fields = ["id", "type", "subtype", "template", "keywords", "created", "modified"]


class TemplateCreateSchema(Schema):
    type = fields.String(
        required=True,
        validate=validate.OneOf(
            ["sms_notification", "email_notification", "push_notification"]
        ),
    )
    subtype = fields.String(required=True)
    message = fields.String(required=True)
    keywords = fields.Nested(KeywordSchema(many=True))


class TemplateUpdateSchema(Schema):
    type = fields.String(
        required=True,
        validate=validate.OneOf(
            ["sms_notification", "email_notification", "push_notification"]
        ),
    )
    subtype = fields.String()
    message = fields.String()
    keywords = fields.Nested(KeywordSchema(many=True))

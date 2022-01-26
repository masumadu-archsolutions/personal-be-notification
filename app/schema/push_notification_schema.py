from marshmallow import (
    Schema,
    ValidationError,
    fields,
    pre_load,
    validate,
    validates_schema,
)

from app.enums import get_notification_subtype, get_notification_type, get_subtype


class PushMessageSchema(Schema):
    id = fields.UUID()
    message_type = fields.String()
    message_subtype = fields.String()
    message_title = fields.String()
    message_body = fields.String()
    created = fields.DateTime()

    @validates_schema
    def validate_subtype(self, field, **kwargs):
        message_subtype = field.get("message_subtype")
        subtype = get_subtype(field.get("message_type"))
        if message_subtype and message_subtype not in subtype:
            raise ValidationError(f"message subtype must be one of {subtype}")

    class Meta:
        fields = [
            "id",
            "message_type",
            "message_subtype",
            "message_title",
            "message_body",
            "created",
        ]
        ordered = True


class CreateMessageSchema(PushMessageSchema):
    message_type = fields.String(
        required=True, validate=validate.OneOf(get_notification_type())
    )
    message_subtype = fields.String(
        required=True, validate=validate.OneOf(get_notification_subtype())
    )
    message_title = fields.String(required=True)
    message_body = fields.String(required=True)

    class Meta:
        fields = [
            "message_type",
            "message_subtype",
            "message_title",
            "message_body",
        ]


class UpdateMessageSchema(PushMessageSchema):
    message_type = fields.String(validate=validate.OneOf(get_notification_type()))
    message_subtype = fields.String(validate=validate.OneOf(get_notification_subtype()))
    message_title = fields.String()
    message_body = fields.String()

    class Meta:
        fields = [
            "message_type",
            "message_subtype",
            "message_title",
            "message_body",
        ]

    @pre_load
    def validate_enum(self, field, **kwargs):
        message_type = field.get("message_type")
        message_subtype = field.get("message_subtype")
        if message_type and not message_subtype or message_subtype and not message_type:
            raise ValidationError("message type and message subtype required")
        return field


class PushMessageMeta(PushMessageSchema):
    message_type = fields.String(
        required=True, validate=validate.OneOf(get_notification_type())
    )
    message_subtype = fields.String(
        required=True, validate=validate.OneOf(get_notification_subtype())
    )

    class Meta:
        fields = ["message_type", "message_subtype"]


class PushSubscriptionSchema(Schema):
    id = fields.UUID()
    endpoint = fields.String()
    auth_keys = fields.String()
    subscription_time = fields.DateTime()
    message_id = fields.String()
    delivered_to_device = fields.Boolean()
    time_delivered = fields.DateTime()

    class Meta:
        ordered = True


class SubscriptionSchema(PushSubscriptionSchema):
    class Meta:
        fields = ["id", "endpoint", "auth_keys", "subscription_time"]


class CreateSubscriptionSchema(PushSubscriptionSchema):
    endpoint = fields.String(required=True)
    auth_keys = fields.String(required=True)

    class Meta:
        fields = ["endpoint", "auth_keys"]


class SendMessageSchema(PushSubscriptionSchema):
    endpoint = fields.String(required=True)
    metadata = fields.Nested(PushMessageMeta, required=True)

    class Meta:
        fields = ["endpoint", "metadata"]

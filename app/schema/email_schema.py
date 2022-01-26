from marshmallow import Schema, fields


class EmailSchema(Schema):
    id = fields.UUID()
    recipient = fields.Str()
    message_type = fields.Str()
    message = fields.Str()
    message_subtype = fields.Str()
    message_template = fields.Str()
    email_client = fields.Str()
    delivered_to_email_client = fields.Boolean()
    reference = fields.Str()
    created = fields.DateTime()

    class Meta:
        ordered = True
        fields = [
            "id",
            "recipient",
            "message_type",
            "message_subtype",
            "message_template",
            "email_client",
            "delivered_to_email_client",
            "reference",
            "created",
        ]

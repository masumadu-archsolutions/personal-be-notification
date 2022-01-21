from marshmallow import Schema, fields


class EmailSchema(Schema):
    id = fields.UUID()
    subject = fields.Str()
    sender = fields.Str()
    recipient = fields.Str()
    message_type = fields.Str()
    message = fields.Str()
    # reference = fields.Str()
    email_client = fields.Str()
    delivered_to_email_client = fields.Boolean()
    created = fields.DateTime()

    class Meta:
        ordered = True

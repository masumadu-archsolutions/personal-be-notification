from marshmallow import Schema, fields


class SMSSchema(Schema):
    id = fields.UUID()
    recipient = fields.Str()
    message_type = fields.Str()
    message = fields.Str()
    reference = fields.Str()
    sms_client = fields.Str()
    delivered_to_sms_client = fields.Boolean()
    created = fields.DateTime()

    class Meta:
        ordered = True

from marshmallow import Schema, fields, validate

class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    capacity = fields.Integer(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class RoomCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    capacity = fields.Integer(required=True)

class RoomUpdateSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=1, max=120))
    capacity = fields.Integer(required=False)

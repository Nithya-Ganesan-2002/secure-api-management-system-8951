from marshmallow import Schema, fields, validate

class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    age = fields.Integer(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class StudentCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    age = fields.Integer(required=True)

class StudentUpdateSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=False)
    age = fields.Integer(required=False)

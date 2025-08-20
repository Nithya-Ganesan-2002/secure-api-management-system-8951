from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    sku = fields.String(required=True, validate=validate.Length(min=1, max=120))
    price = fields.Decimal(required=True, as_string=True)
    stock = fields.Integer(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class ProductCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    sku = fields.String(required=True, validate=validate.Length(min=1, max=120))
    price = fields.Decimal(required=True, as_string=True)
    stock = fields.Integer(required=True)

class ProductUpdateSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=1, max=120))
    sku = fields.String(required=False, validate=validate.Length(min=1, max=120))
    price = fields.Decimal(required=False, as_string=True)
    stock = fields.Integer(required=False)

from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    """Schema for login request."""
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, load_only=True, description="User password", validate=validate.Length(min=6))

class RefreshSchema(Schema):
    """Schema for refresh token request."""
    refresh_token = fields.String(required=True, description="Refresh JWT")

class RegisterSchema(Schema):
    """Schema for user registration."""
    email = fields.Email(required=True, description="User email")
    full_name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    roles = fields.List(fields.String(), required=False, description="List of role names")

class RoleSchema(Schema):
    """Role serialization schema."""
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)

class UserSchema(Schema):
    """User serialization schema."""
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    full_name = fields.String(required=True)
    is_active = fields.Boolean()
    roles = fields.List(fields.Nested(RoleSchema))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class UserCreateSchema(Schema):
    """Schema for creating users (admin)."""
    email = fields.Email(required=True)
    full_name = fields.String(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    roles = fields.List(fields.String(), required=False)

class UserUpdateSchema(Schema):
    """Schema for updating users (admin/self)."""
    full_name = fields.String(required=False)
    password = fields.String(required=False, load_only=True, validate=validate.Length(min=6))
    is_active = fields.Boolean(required=False)
    roles = fields.List(fields.String(), required=False)

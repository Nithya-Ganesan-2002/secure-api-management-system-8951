from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import AuthService
from ..schemas import LoginSchema, RefreshSchema, RegisterSchema, UserSchema

blp = Blueprint("Auth", "auth", url_prefix="/api/auth", description="Authentication endpoints")

auth_service = AuthService()

@blp.route("/register")
class Register(MethodView):
    @blp.arguments(RegisterSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        """Register a new user."""
        user = auth_service.register(
            email=data["email"],
            full_name=data["full_name"],
            password=data["password"],
            roles=data.get("roles"),
        )
        return user

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(200)
    def post(self, data):
        """Login and obtain JWT tokens."""
        access, refresh, user = auth_service.login(data["email"], data["password"])
        return {"access_token": access, "refresh_token": refresh, "user": UserSchema().dump(user)}

@blp.route("/me")
class Me(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        """Get current user's profile using JWT identity."""
        # In real use, fetch user by identity. Here return minimal info from claims.
        user_id = get_jwt_identity()
        # Could query DB to return full user. For now, encourage frontend to call users/<id>.
        return {"id": int(user_id), "email": None, "full_name": "", "is_active": True, "roles": []}

@blp.route("/refresh")
class Refresh(MethodView):
    @blp.arguments(RefreshSchema)
    @blp.response(200)
    def post(self, data):
        """Refresh tokens is usually handled via jwt_required(refresh=True), but keeping schema for completeness."""
        # This implementation expects frontend to store refresh token separately and re-login when needed.
        # Can be extended to accept refresh and issue new access token after verifying it.
        return {"message": "Provide refresh token via Authorization using refresh=True in a real implementation."}

from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask import request
from ..services import UserService
from ..schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from ..utils import role_required
from ..extensions import db
from ..models import User

blp = Blueprint("Users", "users", url_prefix="/api/users", description="User management")

user_service = UserService()

@blp.route("/")
class UsersList(MethodView):
    @jwt_required()
    @role_required(["admin"])
    @blp.response(200)
    def get(self):
        """List users with simple pagination."""
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        items, total = user_service.list(page, per_page)
        return {
            "data": UserSchema(many=True).dump(items),
            "meta": {
                "total": total,
                "page": page,
                "per_page": per_page,
            },
        }

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(UserCreateSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        """Create a new user (admin)."""
        user = user_service.create(
            email=data["email"],
            full_name=data["full_name"],
            password=data["password"],
            roles=data.get("roles"),
        )
        return user

@blp.route("/<int:user_id>")
class UserDetail(MethodView):
    @jwt_required()
    @role_required(["admin"])
    @blp.response(200, UserSchema)
    def get(self, user_id: int):
        """Get user by ID (admin)."""
        user = db.session.get(User, user_id)
        if not user:
            return {"message": "Not found"}, 404
        return user

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, data, user_id: int):
        """Update user (admin)."""
        user = db.session.get(User, user_id)
        if not user:
            return {"message": "Not found"}, 404
        updated = user_service.update(
            user,
            full_name=data.get("full_name"),
            password=data.get("password"),
            is_active=data.get("is_active"),
            roles=data.get("roles"),
        )
        return updated

    @jwt_required()
    @role_required(["admin"])
    @blp.response(204)
    def delete(self, user_id: int):
        """Delete user (admin)."""
        user = db.session.get(User, user_id)
        if not user:
            return {"message": "Not found"}, 404
        user_service.delete(user)
        return ""

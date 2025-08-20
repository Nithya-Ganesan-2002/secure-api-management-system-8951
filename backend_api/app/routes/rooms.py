from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask import request
from ..services import RoomService
from ..schemas import RoomSchema, RoomCreateSchema, RoomUpdateSchema
from ..extensions import db
from ..models import Room
from ..utils import role_required, apply_filters, apply_sorting, paginate_query

blp = Blueprint("Rooms", "rooms", url_prefix="/api/rooms", description="Rooms CRUD")

service = RoomService()

@blp.route("/")
class RoomList(MethodView):
    @jwt_required()
    @role_required(["admin", "user"])
    @blp.response(200)
    def get(self):
        """List rooms with filtering, sorting, and pagination."""
        q = db.session.query(Room)
        filters = {k: request.args.get(k) for k in ["name", "capacity"]}
        q = apply_filters(q, Room, filters)
        q = apply_sorting(q, Room, request.args.get("sort"))
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        items, meta = paginate_query(q, page, per_page)
        return {"data": RoomSchema(many=True).dump(items), "meta": meta}

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(RoomCreateSchema)
    @blp.response(201, RoomSchema)
    def post(self, data):
        """Create room (admin)."""
        return service.create(**data)

@blp.route("/<int:item_id>")
class RoomDetail(MethodView):
    @jwt_required()
    @role_required(["admin", "user"])
    @blp.response(200, RoomSchema)
    def get(self, item_id: int):
        """Get room by id."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        return obj

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(RoomUpdateSchema)
    @blp.response(200, RoomSchema)
    def put(self, data, item_id: int):
        """Update room (admin)."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        return service.update(obj, **data)

    @jwt_required()
    @role_required(["admin"])
    @blp.response(204)
    def delete(self, item_id: int):
        """Delete room (admin)."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        service.delete(obj)
        return ""

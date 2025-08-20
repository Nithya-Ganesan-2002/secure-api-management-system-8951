from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask import request
from ..services import StudentService
from ..schemas import StudentSchema, StudentCreateSchema, StudentUpdateSchema
from ..extensions import db
from ..models import Student
from ..utils import role_required, apply_filters, apply_sorting, paginate_query

blp = Blueprint("Students", "students", url_prefix="/api/students", description="Students CRUD")

service = StudentService()

@blp.route("/")
class StudentList(MethodView):
    @jwt_required()
    @role_required(["admin", "user"])
    @blp.response(200)
    def get(self):
        """List students with filtering, sorting, and pagination."""
        q = db.session.query(Student)
        # filters: name, email, age
        filters = {k: request.args.get(k) for k in ["name", "email", "age"]}
        q = apply_filters(q, Student, filters)
        q = apply_sorting(q, Student, request.args.get("sort"))
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        items, meta = paginate_query(q, page, per_page)
        return {"data": StudentSchema(many=True).dump(items), "meta": meta}

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(StudentCreateSchema)
    @blp.response(201, StudentSchema)
    def post(self, data):
        """Create student (admin)."""
        return service.create(**data)

@blp.route("/<int:item_id>")
class StudentDetail(MethodView):
    @jwt_required()
    @role_required(["admin", "user"])
    @blp.response(200, StudentSchema)
    def get(self, item_id: int):
        """Get student by id."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        return obj

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(StudentUpdateSchema)
    @blp.response(200, StudentSchema)
    def put(self, data, item_id: int):
        """Update student (admin)."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        return service.update(obj, **data)

    @jwt_required()
    @role_required(["admin"])
    @blp.response(204)
    def delete(self, item_id: int):
        """Delete student (admin)."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        service.delete(obj)
        return ""

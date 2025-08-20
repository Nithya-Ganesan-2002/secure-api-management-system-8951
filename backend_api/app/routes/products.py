from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask import request
from ..services import ProductService
from ..schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from ..extensions import db
from ..models import Product
from ..utils import role_required, apply_filters, apply_sorting, paginate_query

blp = Blueprint("Products", "products", url_prefix="/api/products", description="Products CRUD")

service = ProductService()

@blp.route("/")
class ProductList(MethodView):
    @jwt_required()
    @role_required(["admin", "user"])
    @blp.response(200)
    def get(self):
        """List products with filtering, sorting, and pagination."""
        q = db.session.query(Product)
        filters = {k: request.args.get(k) for k in ["name", "sku", "stock"]}
        q = apply_filters(q, Product, filters)
        q = apply_sorting(q, Product, request.args.get("sort"))
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        items, meta = paginate_query(q, page, per_page)
        return {"data": ProductSchema(many=True).dump(items), "meta": meta}

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(ProductCreateSchema)
    @blp.response(201, ProductSchema)
    def post(self, data):
        """Create product (admin)."""
        return service.create(**data)

@blp.route("/<int:item_id>")
class ProductDetail(MethodView):
    @jwt_required()
    @role_required(["admin", "user"])
    @blp.response(200, ProductSchema)
    def get(self, item_id: int):
        """Get product by id."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        return obj

    @jwt_required()
    @role_required(["admin"])
    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def put(self, data, item_id: int):
        """Update product (admin)."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        return service.update(obj, **data)

    @jwt_required()
    @role_required(["admin"])
    @blp.response(204)
    def delete(self, item_id: int):
        """Delete product (admin)."""
        obj = service.get(item_id)
        if not obj:
            return {"message": "Not found"}, 404
        service.delete(obj)
        return ""

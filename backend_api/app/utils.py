from functools import wraps
from typing import Iterable, Tuple
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from sqlalchemy import asc, desc
from sqlalchemy.orm import Query

# PUBLIC_INTERFACE
def role_required(roles: Iterable[str]):
    """Decorator that ensures the JWT contains at least one of the required roles."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt() or {}
            user_roles = set(claims.get("roles", []))
            required = set(roles)
            if not (user_roles & required):
                return jsonify({"message": "Forbidden: insufficient role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def apply_sorting(query: Query, model, sort: str | None) -> Query:
    """Apply sorting on a query. format: 'field' or '-field' for desc."""
    if not sort:
        return query
    field_name = sort.lstrip("-")
    direction = desc if sort.startswith("-") else asc
    if hasattr(model, field_name):
        return query.order_by(direction(getattr(model, field_name)))
    return query

def apply_filters(query: Query, model, filters: dict) -> Query:
    """Apply equality filters for fields present in model."""
    for key, value in filters.items():
        if hasattr(model, key) and value is not None:
            query = query.filter(getattr(model, key) == value)
    return query

def paginate_query(query: Query, page: int, per_page: int) -> Tuple[list, dict]:
    """Return items and pagination metadata."""
    page = max(1, page or 1)
    per_page = min(max(1, per_page or 20), 100)
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total + per_page - 1) // per_page if per_page else 1
    meta = {
        "total": total,
        "total_pages": total_pages,
        "first_page": 1,
        "last_page": total_pages,
        "page": page,
        "previous_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
        "per_page": per_page,
    }
    return items, meta

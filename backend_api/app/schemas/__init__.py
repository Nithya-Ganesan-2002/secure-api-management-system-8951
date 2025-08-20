from .auth import LoginSchema, RefreshSchema, RegisterSchema, RoleSchema, UserSchema, UserCreateSchema, UserUpdateSchema
from .student import StudentSchema, StudentCreateSchema, StudentUpdateSchema
from .room import RoomSchema, RoomCreateSchema, RoomUpdateSchema
from .product import ProductSchema, ProductCreateSchema, ProductUpdateSchema

__all__ = [
    "LoginSchema",
    "RefreshSchema",
    "RegisterSchema",
    "RoleSchema",
    "UserSchema",
    "UserCreateSchema",
    "UserUpdateSchema",
    "StudentSchema",
    "StudentCreateSchema",
    "StudentUpdateSchema",
    "RoomSchema",
    "RoomCreateSchema",
    "RoomUpdateSchema",
    "ProductSchema",
    "ProductCreateSchema",
    "ProductUpdateSchema",
]

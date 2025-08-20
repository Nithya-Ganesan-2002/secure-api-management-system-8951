from typing import Optional, List, Tuple, Optional as _Optional
from flask_jwt_extended import create_access_token, create_refresh_token
from ..extensions import db
from ..models import User, Role

class AuthService:
    """Authentication related operations: register, login, token issue."""
    def register(self, email: str, full_name: str, password: str, roles: _Optional[List[str]] = None) -> User:
        if db.session.query(User).filter_by(email=email).first():
            raise ValueError("Email already registered")
        user = User(email=email, full_name=full_name, is_active=True)
        user.set_password(password)
        assigned_roles: List[Role] = []
        for role_name in (roles or ["user"]):
            role = db.session.query(Role).filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=f"Auto-created role {role_name}")
                db.session.add(role)
            assigned_roles.append(role)
        user.roles = assigned_roles
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, email: str, password: str) -> Tuple[str, str, User]:
        user: Optional[User] = db.session.query(User).filter_by(email=email).first()
        if not user or not user.check_password(password) or not user.is_active:
            raise ValueError("Invalid credentials")
        claims = {"roles": user.role_names, "email": user.email}
        access = create_access_token(identity=str(user.id), additional_claims=claims)
        refresh = create_refresh_token(identity=str(user.id), additional_claims=claims)
        return access, refresh, user

    def tokens_from_user(self, user: User) -> Tuple[str, str]:
        claims = {"roles": user.role_names, "email": user.email}
        return (
            create_access_token(identity=str(user.id), additional_claims=claims),
            create_refresh_token(identity=str(user.id), additional_claims=claims),
        )

from typing import Optional
from ..extensions import db
from ..models import User, Role

class UserService:
    """User management service with role assignment."""
    def get(self, user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)

    def list(self, page: int, per_page: int):
        q = db.session.query(User).order_by(User.id.desc())
        total = q.count()
        items = q.offset((page - 1) * per_page).limit(per_page).all()
        return items, total

    def create(self, email: str, full_name: str, password: str, roles: list[str] | None = None) -> User:
        user = User(email=email, full_name=full_name, is_active=True)
        user.set_password(password)
        assigned_roles = []
        for role_name in roles or ["user"]:
            role = db.session.query(Role).filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=f"Auto-created role {role_name}")
                db.session.add(role)
            assigned_roles.append(role)
        user.roles = assigned_roles
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User, full_name: str | None = None, password: str | None = None, is_active: bool | None = None, roles: list[str] | None = None) -> User:
        if full_name is not None:
            user.full_name = full_name
        if password is not None:
            user.set_password(password)
        if is_active is not None:
            user.is_active = is_active
        if roles is not None:
            assigned_roles = []
            for role_name in roles:
                role = db.session.query(Role).filter_by(name=role_name).first()
                if not role:
                    role = Role(name=role_name, description=f"Auto-created role {role_name}")
                    db.session.add(role)
                assigned_roles.append(role)
            user.roles = assigned_roles
        db.session.commit()
        return user

    def delete(self, user: User) -> None:
        db.session.delete(user)
        db.session.commit()

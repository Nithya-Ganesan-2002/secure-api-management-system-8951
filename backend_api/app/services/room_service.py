from typing import Optional
from ..extensions import db
from ..models import Room

class RoomService:
    """Service for Room entity CRUD."""
    def get(self, id_: int) -> Optional[Room]:
        return db.session.get(Room, id_)

    def create(self, **data) -> Room:
        room = Room(**data)
        db.session.add(room)
        db.session.commit()
        return room

    def update(self, room: Room, **data) -> Room:
        for k, v in data.items():
            setattr(room, k, v)
        db.session.commit()
        return room

    def delete(self, room: Room) -> None:
        db.session.delete(room)
        db.session.commit()

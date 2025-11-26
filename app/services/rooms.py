import uuid
from sqlalchemy.orm import Session

from ..models.room import Room


def create_room(db: Session) -> Room:
    """Create a new room with a unique ID."""
    room_id = str(uuid.uuid4())
    room = Room(id=room_id, code="")
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def get_room(db: Session, room_id: str) -> Room | None:
    """Get a room by ID."""
    return db.query(Room).filter(Room.id == room_id).first()


def update_room_code(db: Session, room_id: str, code: str) -> Room | None:
    """Update the code content of a room."""
    room = get_room(db, room_id)
    if room:
        room.code = code
        db.commit()
        db.refresh(room)
    return room


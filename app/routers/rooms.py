from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas.rooms import RoomCreateResponse, RoomResponse
from ..services.rooms import create_room, get_room

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=RoomCreateResponse)
def create_new_room(db: Session = Depends(get_db)):
    """Create a new room and return its ID."""
    room = create_room(db)
    return RoomCreateResponse(roomId=room.id)


@router.get("/{room_id}", response_model=RoomResponse)
def get_room_by_id(room_id: str, db: Session = Depends(get_db)):
    """Get room details by ID."""
    room = get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return RoomResponse(id=room.id, code=room.code)


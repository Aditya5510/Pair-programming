import json
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services.rooms import get_room, update_room_code

router = APIRouter()

active_connections: Dict[str, Set[WebSocket]] = {}


class ConnectionManager:
    """Manages WebSocket connections for real-time collaboration."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        """Accept a new WebSocket connection and add it to the room."""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        """Remove a WebSocket connection from the room."""
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast_to_room(self, room_id: str, message: dict, sender: WebSocket = None):
        """Broadcast a message to all connections in a room, except the sender."""
        if room_id not in self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections[room_id]:
            if connection != sender:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)
        
        for conn in disconnected:
            self.disconnect(conn, room_id)


manager = ConnectionManager()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    
    db = SessionLocal()
    try:
        room = get_room(db, room_id)
        if room:
            await websocket.send_json({
                "type": "code_update",
                "code": room.code
            })
    except Exception as e:
        print(f"Error loading room code: {e}")
    finally:
        db.close()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "code_update":
                code = message.get("code", "")
                
                db = SessionLocal()
                try:
                    update_room_code(db, room_id, code)
                except Exception as e:
                    print(f"Error updating room code in DB: {e}")
                finally:
                    db.close()
                
                await manager.broadcast_to_room(
                    room_id,
                    {"type": "code_update", "code": code},
                    sender=websocket
                )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    except Exception as e:
        manager.disconnect(websocket, room_id)
        print(f"WebSocket error: {e}")


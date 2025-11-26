from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, rooms, autocomplete, websocket
from .db import init_db

app = FastAPI(
    title="Realtime Pair Programming Backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(health.router)
app.include_router(rooms.router)
app.include_router(autocomplete.router)
app.include_router(websocket.router)

@app.get("/")
def root() -> dict:
    return {"message": "Backend is running"}

# Realtime Pair Programming Editor

A simplified real time collab code editor where multiple users can join the same room, edit code simultaneously, and see each other's changes instantly.

## Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **WebSockets** - Real-time bidirectional communication
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** (Supabase) - Database for room and code persistence
- **Gemini API** (google-genai SDK) - For AI autocomplete (optional, mocked by default)

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── config.py        # Configuration and environment variables
│   ├── db.py            # Database connection and session management
│   ├── routers/         # API route handlers
│   │   ├── rooms.py     # Room management endpoints
│   │   ├── autocomplete.py  # Autocomplete endpoint
│   │   ├── websocket.py # WebSocket handler
│   │   └── health.py    # Health check endpoint
│   ├── services/        # Business logic
│   │   └── rooms.py     # Room service functions
│   ├── models/          # SQLAlchemy database models
│   │   └── room.py      # Room model
│   └── schemas/         # Pydantic schemas
│       └── rooms.py     # Request/response schemas
├── requirements.txt     # Python dependencies
```

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repo-url>
cd pair-programming
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=your_supabase_connection_string
GEMINI_API_KEY=your_gemini_api_key
```

**Note:** If `DATABASE_URL` is not set, the application will automatically use SQLite for development.

### 4. Run Server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

## API Overview

### Create Room

**Endpoint:** `POST /rooms`

**Response:**

```json
{
  "roomId": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Get Room

**Endpoint:** `GET /rooms/{room_id}`

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "code": ""
}
```

### Autocomplete

**Endpoint:** `POST /autocomplete`

**Request:**

```json
{
  "code": "def ",
  "cursorPosition": 4,
  "language": "python"
}
```

**Response:**

```json
{
  "suggestion": "function_name():"
}
```

### WebSocket Connection

**Endpoint:** `ws://localhost:8000/ws/{roomId}`

**Send Message:**

```json
{
  "type": "code_update",
  "code": "def hello():\n    print('Hello, World!')"
}
```

**Receive Message:**

```json
{
  "type": "code_update",
  "code": "..."
}
```

## Architecture & Design Choices

### Real Time Collab

- Uses WebSocket connections for instant code synchronization
- Each room maintains a set of active WebSocket connections
- Code updates are broadcast to all clients in the same room (except sender)
- Database is updated on each code change for persistence

### Database

- PostgreSQL (Supabase) for production
- SQLite fallback for development when `DATABASE_URL` is not set
- Room state (code content) is persisted in the database

### Autocomplete

- Currently uses rule-based mocked suggestions
- Can be enhanced with Gemini API by setting `GEMINI_API_KEY`

## Limitations

- Simple last-write-wins conflict
- No user authentication
- Database writes on every keystroke

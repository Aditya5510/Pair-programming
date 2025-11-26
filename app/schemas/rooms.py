from pydantic import BaseModel


class RoomCreateResponse(BaseModel):
    roomId: str


class RoomResponse(BaseModel):
    id: str
    code: str


class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"


class AutocompleteResponse(BaseModel):
    suggestion: str


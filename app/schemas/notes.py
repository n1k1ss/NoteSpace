from pydantic import BaseModel

class CreateNoteRequest(BaseModel):
    title: str
    text: str
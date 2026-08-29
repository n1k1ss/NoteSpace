from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(
    title="NoteSpace"
)

app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)

class Note(BaseModel):
    title: str
    text: str


notes = []

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/api/notes")
def write_note(note: Note):
    notes.append(note)

    return {
        "message": "Note created",
        "note": {
            "title": note.title,
            "text": note.text
        }
    }

@app.get("/api/notes")
def get_notes():
    return { "notes": notes }

@app.get("/api/notes/{index}")
def get_notes(index: int):
    return { "note": notes[index] }
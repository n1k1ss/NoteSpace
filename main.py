from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, RedirectResponse
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

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


notes = []
users = []

@app.get("/")
def home(request: Request):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/register")

    return FileResponse("index.html")

@app.get("/login")
def login():
    return FileResponse("login.html")

@app.post("/api/login")
def login(user: UserLogin, response: Response):

    for registered_user in users:

        if (
            registered_user["username"] == user.username
            and registered_user["password"] == user.password
        ):

            response.set_cookie(
                key="user_id",
                value=str(registered_user["id"]),
                httponly=True
            )

            return {
                "message": "Login successful",
                "redirect": "/"
            }

    return {
        "message": "Invalid username or password"
    }

@app.get("/register")
def register():
    return FileResponse("register.html")

@app.post("/api/register")
def register(user: UserRegister, response: Response):
    user_id = len(users) + 1

    users.append({
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "password": user.password
    })

    response.set_cookie(
        key="user_id",
        value=str(user_id),
        httponly=True
    )

    return {
        "message": "Account created",
        "redirect": "/"
    }

@app.post("/api/notes")
def write_note(note: Note, request: Request):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return {
            "message": "You are not logged in"
        }

    notes.append({
        "user_id": int(user_id),
        "title": note.title,
        "text": note.text
    })

    return {
        "message": "Note created",
        "note": {
            "title": note.title,
            "text": note.text
        }
    }

@app.get("/api/notes")
def get_notes(request: Request):

    user_id = request.cookies.get("user_id")

    if not user_id:
        return {
            "message": "You are not logged in"
        }

    user_notes = []

    for note in notes:
        if note["user_id"] == int(user_id):
            user_notes.append(note)

    return {
        "notes": user_notes
    }

@app.get("/api/notes/{index}")
def get_note(index: int, request: Request):

    user_id = request.cookies.get("user_id")

    if not user_id:
        return {
            "message": "You are not logged in"
        }

    note = notes[index]

    if note["user_id"] != int(user_id):
        return {
            "message": "Access denied"
        }

    return {
        "note": note
    }
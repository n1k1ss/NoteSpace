from fastapi import FastAPI, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import router as auth_router
from app.api.notes import router as notes_router
from app.db.dependencies import get_db
from app.db.models.user import User
from app.db.models.sessions import Session
from app.security.dependencies import get_optional_user

app = FastAPI(
    title="NoteSpace"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/")
async def home(
    user: User | None = Depends(get_optional_user),
):
    if user is None:
        return RedirectResponse("/register")

    return FileResponse("app/index.html")

@app.get("/register")
async def register():
    return FileResponse("app/register.html")

@app.get("/login")
async def login():
    return FileResponse("app/login.html")
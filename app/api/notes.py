from fastapi import APIRouter, Depends
from app.schemas.notes import CreateNoteRequest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.dependencies import get_db
from app.db.models.user import User
from app.db.models.notes import Note
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/api/notes",
    tags=["notes"],
)

@router.post("/create", status_code=201)
async def create_note(
    data: CreateNoteRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    note = Note(
        title=data.title,
        text=data.text,
        user_id=user.id,
    )

    db.add(note)

    await db.commit()

    return {
        "message": "Note created",
        "title": data.title,
        "text": data.text,
        "user_id": user.id,
    }



@router.get("/check")
async def get_notes(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Note).where(
            Note.user_id == user.id
        )
    )

    notes = result.scalars().all()

    return { "notes": notes }
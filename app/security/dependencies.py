
from fastapi import Request, HTTPException, Depends

from app.db.models.user import User
from app.db.models.sessions import Session
from app.db.dependencies import get_db

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import datetime, timezone

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    session_token = request.cookies.get("session_token")

    if session_token is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    result = await db.execute(
        select(Session).where(
            Session.token == session_token
        )
    )
    session = result.scalar_one_or_none()

    if session is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid session"
            )

    if session.expires_at < datetime.now(timezone.utc):
        await db.delete(session)
        await db.commit()

        raise HTTPException(
        status_code=401,
        detail="Session expired",
    )

    result = await db.execute(
        select(User)
        .options(selectinload(User.notes)).where(
            User.id == session.user_id
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
    )

    return user



async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    token = request.cookies.get("session_token")

    if token is None:
        return None

    result = await db.execute(
        select(Session).where(
            Session.token == token
        )
    )

    session = result.scalar_one_or_none()

    if session is None:
        return None

    if session.expires_at <= datetime.now(timezone.utc):
        await db.delete(session)
        await db.commit()
        return None

    result = await db.execute(
        select(User)
        .options(selectinload(User.notes))
        .where(User.id == session.user_id)
    )

    return result.scalar_one_or_none()
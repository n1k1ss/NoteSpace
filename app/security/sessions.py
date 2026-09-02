import secrets

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.sessions import Session



SESSION_LIFETIME = timedelta(days=30)


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


async def create_session(
        db: AsyncSession,
        user_id: int
) -> str:
    token = generate_session_token()

    session = Session(
        token=token,
        user_id=user_id,
        expires_at=datetime.now(timezone.utc) + SESSION_LIFETIME,
    )

    db.add(session)
    await db.commit()

    return token
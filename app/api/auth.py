from fastapi import APIRouter, Depends, HTTPException, Response

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.dependencies import get_db
from app.schemas.auth import RegisterRequest, LoginRequest
from app.security.passwords import hash_password
from app.security.sessions import create_session
from app.security.passwords import verify_password


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/register", status_code=201)
async def register(
    data: RegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(or_(
                User.username == data.username,
                User.email == data.email
            )
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    session_token = await create_session(
        db,
        user.id,
    )

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
    )

    return {
        "message": "Account created",
        "user_id": user.id,
        "redirect": "/"
    }



@router.post("/login", status_code=201)
async def login(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(
            User.email == data.email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    session_token = await create_session(
        db,
        user.id,
    )

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
    )

    return {
        "message": "Login successful",
        "redirect": "/"
    }
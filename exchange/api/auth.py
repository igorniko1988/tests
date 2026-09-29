from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from exchange.api.deps import Session, UserId
from exchange.db import User
from exchange.errors import ApiError
from exchange.schemas import LoginRequest, RegisterRequest, TokenOut, UserOut
from exchange.security import create_access_token, hash_password, verify_password

router = APIRouter(tags=["auth"])


@router.post("/auth/register", status_code=201, response_model=UserOut)
async def register(body: RegisterRequest, session: Session):
    user = User(email=body.email.lower(), password_hash=hash_password(body.password))
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise ApiError(409, "email_taken", "User with this email already exists") from None
    return user


@router.post("/auth/login", response_model=TokenOut)
async def login(body: LoginRequest, session: Session):
    user = await session.scalar(select(User).where(User.email == body.email.lower()))
    if user is None or not verify_password(body.password, user.password_hash):
        raise ApiError(401, "invalid_credentials", "Invalid email or password")
    token, ttl = create_access_token(user.id)
    return TokenOut(access_token=token, expires_in=ttl)


@router.get("/me", response_model=UserOut)
async def me(user_id: UserId, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise ApiError(401, "unauthorized", "User not found")
    return user

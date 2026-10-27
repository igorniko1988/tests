import time
import uuid
from collections import defaultdict, deque

import jwt
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from exchange.api.deps import Session, UserId
from exchange.config import settings
from exchange.db import RefreshToken, SessionLocal, User
from exchange.errors import ApiError
from exchange.schemas import (
    LoginRequest,
    ProfileOut,
    RefreshRequest,
    RegisterRequest,
    TokenOut,
    UpdateProfileRequest,
    UserOut,
)
from exchange.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)

router = APIRouter(tags=["auth"])

# Неудачные входы по email: защита от перебора пароля (в памяти процесса)
_login_failures: dict[str, deque[float]] = defaultdict(deque)


def _check_login_rate(email: str) -> None:
    failures = _login_failures[email]
    now = time.monotonic()
    while failures and now - failures[0] > settings.login_failure_window:
        failures.popleft()
    if len(failures) >= settings.login_max_failures:
        retry_after = int(settings.login_failure_window - (now - failures[0])) + 1
        raise ApiError(
            429,
            "too_many_attempts",
            "Too many failed login attempts, try later",
            headers={"Retry-After": str(retry_after)},
        )


async def _issue_tokens(session, user_id: uuid.UUID) -> TokenOut:
    access, ttl = create_access_token(user_id)
    refresh, jti = create_refresh_token(user_id)
    session.add(RefreshToken(jti=jti, user_id=user_id))
    await session.commit()
    return TokenOut(access_token=access, refresh_token=refresh, expires_in=ttl)


async def ensure_admin() -> None:
    async with SessionLocal() as session:
        email = settings.admin_email.lower()
        if await session.scalar(select(User).where(User.email == email)):
            return
        session.add(
            User(email=email, password_hash=hash_password(settings.admin_password), role="admin")
        )
        try:
            await session.commit()
        except IntegrityError:
            # Второй воркер успел создать админа раньше
            await session.rollback()


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
    email = body.email.lower()
    _check_login_rate(email)
    user = await session.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(body.password, user.password_hash):
        _login_failures[email].append(time.monotonic())
        raise ApiError(401, "invalid_credentials", "Invalid email or password")
    _login_failures.pop(email, None)
    if user.blocked:
        raise ApiError(403, "user_blocked", "User is blocked")
    return await _issue_tokens(session, user.id)


@router.post("/auth/refresh", response_model=TokenOut)
async def refresh(body: RefreshRequest, session: Session):
    try:
        user_id, jti = decode_refresh_token(body.refresh_token)
    except jwt.ExpiredSignatureError:
        raise ApiError(401, "token_expired", "Refresh token expired") from None
    except (jwt.InvalidTokenError, ValueError, KeyError):
        raise ApiError(401, "unauthorized", "Invalid refresh token") from None
    saved = await session.get(RefreshToken, jti)
    if saved is None:
        raise ApiError(401, "unauthorized", "Invalid refresh token")
    # Ротация: старый refresh-токен больше не нужен
    saved.revoked = True
    user = await session.get(User, user_id)
    if user is None or user.blocked:
        raise ApiError(403, "user_blocked", "User is blocked")
    return await _issue_tokens(session, user_id)


@router.get("/me", response_model=ProfileOut)
async def me(user_id: UserId, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise ApiError(401, "unauthorized", "User not found")
    return user


@router.patch("/me", response_model=ProfileOut)
async def update_me(body: UpdateProfileRequest, user_id: UserId, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise ApiError(401, "unauthorized", "User not found")
    for field, value in body.model_dump().items():
        if hasattr(user, field):
            setattr(user, field, value)
    await session.commit()
    return user

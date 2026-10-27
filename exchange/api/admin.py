import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select

from exchange.api.deps import Session, UserId
from exchange.db import User
from exchange.errors import ApiError
from exchange.schemas import AdminUserOut

router = APIRouter(tags=["admin"])


async def admin_user_id(user_id: UserId, session: Session) -> uuid.UUID:
    user = await session.get(User, user_id)
    if user is None or user.role != "admin":
        raise ApiError(403, "forbidden", "Admin role required")
    return user_id


AdminId = Annotated[uuid.UUID, Depends(admin_user_id)]


async def _get_user(session, user_id: uuid.UUID) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise ApiError(404, "user_not_found", "User not found")
    return user


@router.get("/admin/users", response_model=list[AdminUserOut])
async def list_users(_: AdminId, session: Session):
    return list(await session.scalars(select(User).order_by(User.created_at.desc()).limit(100)))


@router.post("/admin/users/{user_id}/block", response_model=AdminUserOut)
async def block_user(user_id: uuid.UUID, _: UserId, session: Session):
    user = await _get_user(session, user_id)
    user.blocked = True
    await session.commit()
    return user


@router.post("/admin/users/{user_id}/unblock", response_model=AdminUserOut)
async def unblock_user(user_id: uuid.UUID, _: AdminId, session: Session):
    user = await _get_user(session, user_id)
    user.blocked = False
    await session.commit()
    return user

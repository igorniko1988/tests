from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    """Ответ POST /auth/register."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    email: EmailStr
    created_at: datetime


class Profile(User):
    """Ответ GET /me: пользователь + профиль и роль."""

    display_name: str | None
    role: Literal["user", "admin"]

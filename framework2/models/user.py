import uuid

from pydantic import AwareDatetime, BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    email: str
    created_at: AwareDatetime


class Token(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str
    expires_in: int

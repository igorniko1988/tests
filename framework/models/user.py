import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: uuid.UUID
    email: str
    created_at: datetime
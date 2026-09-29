import uuid
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from exchange.db import get_session
from exchange.errors import ApiError
from exchange.security import decode_access_token

Session = Annotated[AsyncSession, Depends(get_session)]
_bearer = HTTPBearer(auto_error=False)


async def current_user_id(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> uuid.UUID:
    if creds is None:
        raise ApiError(401, "unauthorized", "Missing bearer token")
    try:
        return decode_access_token(creds.credentials)
    except jwt.ExpiredSignatureError:
        raise ApiError(401, "token_expired", "Access token expired") from None
    except (jwt.InvalidTokenError, ValueError, KeyError):
        raise ApiError(401, "unauthorized", "Invalid access token") from None


UserId = Annotated[uuid.UUID, Depends(current_user_id)]

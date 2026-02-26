from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

from edutracker.api.deps.get_auth_db import get_auth_db
from edutracker.infrastructure.repositories.auth_user_repository import AuthUserRepository
from edutracker.core.config import settings
from edutracker.application.common.exceptions import (
    InvalidAccessTokenError,
    AccessTokenExpiredError,
    InvalidTokenPayloadError,
    UserNotFoundError,
    InactiveUserError,
)

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_auth_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,            
            algorithms=[settings.JWT_ALG],  
        )
    except jwt.ExpiredSignatureError as e:
        raise AccessTokenExpiredError() from e
    except jwt.InvalidTokenError as e:
        raise InvalidAccessTokenError() from e

    user_id = payload.get("user_id") or payload.get("sub")
    if not user_id:
        raise InvalidTokenPayloadError()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise InvalidTokenPayloadError()

    user = AuthUserRepository(db).get_by_id(user_id)
    if not user:
        raise UserNotFoundError()
    if not user.is_active:
        raise InactiveUserError()

    return user
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from jwt import DecodeError
from edutracker.core.config import settings

from edutracker.api.deps.get_auth_db import get_auth_db
from edutracker.api.v1.schemas.auth import GoogleLoginIn, RefreshIn, AccessOut
from edutracker.application.services.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/google", response_model=AccessOut)
def login_google(payload: GoogleLoginIn, response: Response, db : Session = Depends(get_auth_db)):
    service = AuthService(db)
    result = service.login_with_google_id_token(id_token=payload.id_token)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=False, # Потмі поміняю
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TLL_DAYS,
        path="api/v1/routers/auth",
    )

    return AccessOut(access_token=result.a)
    

@router.post("/refresh", response_model=AccessOut)
def refresh(payload: RefreshIn, db: Session = Depends(get_auth_db)) -> AccessOut:
    service = AuthService(db)
    access = service.refresh_access_token(refresh_token=payload.refresh_token)
    return AccessOut(access_token=access)
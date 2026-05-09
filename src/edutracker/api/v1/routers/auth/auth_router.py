from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
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
        path="/api/v1/auth",
    )

    return AccessOut(access_token=result.access_token)
    

@router.post("/refresh", response_model=AccessOut)
def refresh(request: Request, db: Session = Depends(get_auth_db)) -> AccessOut:
    rt = request.cookies.get("refresh_token")
    if not rt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token"
        )

    service = AuthService(db)
    access = service.refresh_access_token(refresh_token=rt)
    return AccessOut(access_token=access)


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_auth_db)):
    rt = request.cookies.get("refresh_token")
    if rt: 
        AuthService(db).logout(refresh_token=rt)

    response.delete_cookie(key="refresh_token", path="/api/v1/auth")
    return {"ok": True}
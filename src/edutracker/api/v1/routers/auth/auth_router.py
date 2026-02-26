from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jwt import DecodeError

from edutracker.api.deps.get_auth_db import get_auth_db
from edutracker.api.v1.schemas.auth import GoogleLoginIn, TokenOut, RefreshIn, AccessOut
from edutracker.application.services.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/google", response_model=TokenOut)
def login_google(payload: GoogleLoginIn, db: Session = Depends(get_auth_db)) -> TokenOut:
    try:
        service = AuthService(db)
        result = service.login_with_google_id_token(id_token=payload.id_token)
        return TokenOut(access_token=result.access_token, refresh_token=result.refresh_token, token_type=result.token_type)
    except (ValueError, DecodeError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    

@router.post("/refresh", response_model=AccessOut)
def refresh(payload: RefreshIn, db: Session = Depends(get_auth_db)) -> AccessOut:
    try:
        service = AuthService(db)
        access = service.refresh_access_token(refresh_token=payload.refresh_token)
        return AccessOut(access_token=access)
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
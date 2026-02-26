from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from edutracker.infrastructure.repositories.auth_user_repository import AuthUserRepository
from edutracker.infrastructure.repositories.refresh_token_repository import RefreshTokenRepository
from edutracker.infrastructure.sucurity.google_id_token_verifier import GoogleIdTokenVerifier
from edutracker.infrastructure.sucurity.jwt_provider import JwtProvider
from edutracker.application.common.tokens import new_refresh_token, hash_token
from edutracker.application.dto.auth_token_dto import AuthTokensResult
from edutracker.core.config import settings



class AuthService:
    def __init__(self, db: Session):
        self._db = db
        self._users = AuthUserRepository(db)
        self._refresh = RefreshTokenRepository(db)
        self._google = GoogleIdTokenVerifier(settings.GOOGLE_CLIENT_ID)
        self._jwt = JwtProvider()


    def login_with_google_id_token(self, *, id_token: str) -> AuthTokensResult:
        ident = self._google.verify(id_token)

        user = self._users.get_by_google_sub(ident.sub)
        if not user:
            user = self._users.create_user(email=ident.email, google_sub=ident.sub, role="teacher")

        if not user.is_active:
            raise PermissionError("User is inactive")
        
        access = self._jwt.create_access_token(user_id=user.id, email=user.email, role=user.role)

        refresh_plain = new_refresh_token()
        refresh_hash = hash_token(refresh_plain)
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TLL_DAYS)

        self._refresh.create(user_id=user.id, token_hash=refresh_hash, expires_at=expires_at)

        return AuthTokensResult(access_token=access, refresh_token=refresh_plain)
    
    def refresh_access_token(self, *, refresh_token: str) -> str:
        now = datetime.now(timezone.utc)
        token_hash = hash_token(refresh_token)

        rt = self._refresh.get_valid(token_hash=token_hash, now=now)

        if not rt:
            raise PermissionError("Invalid refresh token")
        
        user = rt.user
        
        if not user.is_active:
            raise PermissionError("User is inactive")
        
        return self._jwt.create_access_token(user_id=user.id, email=user.email, role=user.role)
    
    def logout(self, *, refresh_token: str) -> None:
        now = datetime.now(timezone.utc)
        token_hash = hash_token(refresh_token)
        self._refresh.revoke(token_hash=token_hash, now=now)


from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.Auth.auth_model import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(self, *, user_id: int, token_hash: str, expires_at: datetime) -> RefreshToken | None:
        rt = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        self._db.add(rt)
        self._db.commit()
        self._db.refresh(rt)

        return rt
    
    def get_valid(self, *, token_hash: str, now: datetime) -> RefreshToken | None:
        stmt = (
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .where(RefreshToken.revoked_at.is_(None))
            .where(RefreshToken.expires_at > now)
        )
        return self._db.execute(stmt).scalar_one_or_none()
    
    def revoke(self, *, token_hash: str, now: datetime) -> None:
        rt = self.get_valid(token_hash=token_hash, now=now)
        if not rt:
            return 
        rt.revoked_at = now
        self._db.commit()

from sqlalchemy import select
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.Auth.auth_model import AuthUser


class AuthUserRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, user_id: int):
        return self._db.query(AuthUser).filter(AuthUser.id == user_id).first()

    def get_by_google_sub(self, google_sub: str) -> AuthUser | None:
        stmt = select(AuthUser).where(AuthUser.google_sub == google_sub)
        return self._db.execute(stmt).scalar_one_or_none()
    
    def get_by_email(self, email: str) -> AuthUser | None:
        stmt = select(AuthUser).where(AuthUser.email == email)
        return self._db.execute(stmt).scalar_one_or_none()
    
    def create_user(self, *, email: str, google_sub: str, role: str = "teacher") -> AuthUser:
        user = AuthUser(email=email, google_sub=google_sub, role=role, is_active=True)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

        return user
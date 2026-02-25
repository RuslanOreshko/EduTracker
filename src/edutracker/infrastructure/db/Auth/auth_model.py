from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edutracker.infrastructure.db.Auth.auth_base import AuthBase


class AuthUser(AuthBase):
    __tablename__ = "auth_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    google_sub: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    role: Mapped[str] = mapped_column(String, nullable=False, default="teacher")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")


class RefreshToken((AuthBase)):
    __tablename__ = "auth_refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(Text, nullable=False, index=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped["AuthUser"] = relationship(back_populates="refresh_tokens")
from datetime import datetime, timedelta, timezone
import jwt

from edutracker.core.config import settings


class JwtProvider:
    def create_access_token(self, *, user_id: int, email: str, role: str) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=settings.JWT_ACCESS_TLL_MIN)
        payload = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=15)).timestamp()),
        }

        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    
    def verify_access_token(self, token: str) -> dict:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
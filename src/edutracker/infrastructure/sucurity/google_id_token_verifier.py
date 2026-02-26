import time
import logging
import urllib.request
import json
from dataclasses import dataclass
from typing import Any

import jwt
from jwt import PyJWKClient

from edutracker.core.config import settings

logger = logging.getLogger(__name__)


GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUERS = {"https://accounts.google.com", "accounts.google.com"}


@dataclass(frozen=True, slots=True)
class GoogleIdentity:
    sub: str
    email: str
    email_verified: bool
    hd: str | None

# Перевірка пошти 
class GoogleIdTokenVerifier:
    def __init__(self, client_id: str) -> None:
        self._client_id = client_id
        self._jwk_client = PyJWKClient(GOOGLE_JWKS_URL)

    def verify(self, id_token: str) -> GoogleIdentity:
        signing_key = self._jwk_client.get_signing_key_from_jwt(id_token).key

        claims: dict[str, Any] = jwt.decode(
            id_token,
            signing_key,
            algorithms=["RS256"],
            options={"require": ["exp", "iat", "sub"]},
            audience=self._client_id,  # твій GOOGLE_CLIENT_ID
            issuer=GOOGLE_ISSUERS,
        )

        iss = claims.get("iss")
        if iss not in GOOGLE_ISSUERS:
            raise ValueError("Invalid issuer")
        
        email = str(claims.get("email") or "").lower()
        email_verified = bool(claims.get("email_verified", False))
        sub = str(claims.get("sub") or "")
        hd = claims.get("hd")

        if not sub or not email:
            raise ValueError("Missing required claims")
        
        if not email_verified:
            raise ValueError("Email is not verified")
        
        allowed = settings.AUTH_ALLOWED_DOMAIM.lower()
        if not email.endswith("@" + allowed):
            raise ValueError("Not a corporate account")
        
        return GoogleIdentity(
            sub=sub,
            email=email,
            email_verified=email_verified,
            hd=hd if isinstance(hd, str) else None
        )
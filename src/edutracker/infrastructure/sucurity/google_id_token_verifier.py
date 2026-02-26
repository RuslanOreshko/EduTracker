import time
import logging
import urllib.request
import json
from dataclasses import dataclass
from typing import Any

import jwt
from jwt import PyJWKClient, ExpiredSignatureError, InvalidTokenError

from edutracker.core.config import settings

from edutracker.application.common.exceptions import InvalidGoogleTokenError

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
        try:
            signing_key = self._jwk_client.get_signing_key_from_jwt(id_token).key

            claims: dict[str, Any] = jwt.decode(
                id_token,
                signing_key,
                algorithms=["RS256"],
                options={"require": ["exp", "iat", "sub"]},
                audience=self._client_id,  # твій GOOGLE_CLIENT_ID
                issuer=GOOGLE_ISSUERS,
            )


        except ExpiredSignatureError as e:
                raise InvalidGoogleTokenError("Google token expired") from e

        except InvalidTokenError as e:
            raise InvalidGoogleTokenError("Invalid Google token") from e

        except Exception as e:
            raise InvalidGoogleTokenError("Google token verification failed") from e
        
        email = str(claims.get("email") or "").lower()
        email_verified = bool(claims.get("email_verified", False))
        sub = str(claims.get("sub") or "")
        hd = claims.get("hd")

        if not sub or not email:
            raise InvalidGoogleTokenError("Missing required claims")
        
        if not email_verified:
            raise InvalidGoogleTokenError("Email is not verified")
        
        
        return GoogleIdentity(
            sub=sub,
            email=email,
            email_verified=email_verified,
            hd=hd if isinstance(hd, str) else None
        )
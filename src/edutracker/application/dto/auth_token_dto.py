from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthTokensResult:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
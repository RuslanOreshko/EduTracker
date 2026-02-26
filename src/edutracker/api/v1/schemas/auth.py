from pydantic import BaseModel, field_validator


class GoogleLoginIn(BaseModel):
    id_token: str
    @field_validator("id_token")
    @classmethod
    def looks_like_jwt(cls, v: str) -> str:
        v = v.strip()
        if v.count(".") != 2:
            raise ValueError("id_token must be a JWT (three segments separated by dots)")
        return v

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshIn(BaseModel):
    refresh_token: str

class AccessOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
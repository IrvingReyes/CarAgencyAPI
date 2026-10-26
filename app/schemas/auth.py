from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Exposes fields in camelCase (refresh_token -> refreshToken), the format API clients expect."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRefreshRequest(CamelModel):
    token: str
    refresh_token: str


class TokenData(CamelModel):
    token: str
    refresh_token: str
    token_expiry_time: datetime
    refresh_token_expiry_time: datetime


class TokenResponse(BaseModel):
    data: TokenData

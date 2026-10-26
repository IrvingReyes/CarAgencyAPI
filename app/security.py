from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt
from pwdlib import PasswordHash

from app.config import settings

ALGORITHM = "HS256"

TokenType = Literal["access", "refresh"]

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_token(subject: str, token_type: TokenType) -> tuple[str, datetime]:
    """Return a signed JWT and its expiration time."""
    if token_type == "access":
        lifetime = timedelta(minutes=settings.access_token_expire_minutes)
    else:
        lifetime = timedelta(days=settings.refresh_token_expire_days)
    now = datetime.now(timezone.utc)
    expires_at = now + lifetime
    payload = {"sub": subject, "type": token_type, "iat": now, "exp": expires_at}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM), expires_at


def decode_token(token: str, token_type: TokenType, verify_exp: bool = True) -> str:
    """Return the token subject. Raises jwt.InvalidTokenError if invalid, expired or of another type."""
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[ALGORITHM],
        options={"verify_exp": verify_exp, "require": ["sub", "type", "exp"]},
    )
    if payload["type"] != token_type:
        raise jwt.InvalidTokenError("Wrong token type")
    return payload["sub"]

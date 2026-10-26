import jwt
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.database import SessionDep
from app.models import UserDB
from app.schemas.auth import TokenData, TokenRefreshRequest, TokenRequest, TokenResponse
from app.security import create_token, decode_token, verify_password

router = APIRouter(prefix="/tokens", tags=["auth"])


@router.post("", response_model=TokenResponse)
def create_tokens(payload: TokenRequest, session: SessionDep):
    user = session.exec(select(UserDB).where(UserDB.email == payload.email)).first()
    if user is None or not user.is_active or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return issue_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
def refresh_tokens(payload: TokenRefreshRequest, session: SessionDep):
    invalid = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    try:
        user_id = decode_token(payload.refresh_token, "refresh")
        # The access token may already be expired; it only has to be genuine and belong to the same user
        access_user_id = decode_token(payload.token, "access", verify_exp=False)
    except jwt.InvalidTokenError:
        raise invalid
    if user_id != access_user_id:
        raise invalid
    user = session.get(UserDB, int(user_id))
    if user is None or not user.is_active:
        raise invalid
    return issue_tokens(user)


def issue_tokens(user: UserDB) -> TokenResponse:
    token, token_expiry_time = create_token(str(user.id), "access")
    refresh_token, refresh_token_expiry_time = create_token(str(user.id), "refresh")
    return TokenResponse(
        data=TokenData(
            token=token,
            refresh_token=refresh_token,
            token_expiry_time=token_expiry_time,
            refresh_token_expiry_time=refresh_token_expiry_time,
        )
    )

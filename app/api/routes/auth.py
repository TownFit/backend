from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.schemas import UserCreate
from app.utils.google_auth import getGoogleToken, getGoogleUserName
from app.utils.google_profile import GoogleProfile
from app.core.config import settings
from app.core.db import get_db
from app import crud
from app.user import create_jwt_for_user

router = APIRouter(tags=["auth"])


@router.get(
    "/auth/google/callback",
    status_code=status.HTTP_302_FOUND,
    response_class=RedirectResponse,
    responses={302: {"description": "로그인 후 프론트엔드로 리다이렉트"}},
)
def google_callback(
    request: Request, code: str, dbSession: Annotated[Session, Depends(get_db)]
) -> RedirectResponse:
    """
    Google 로그인 Callback

    - ❌❌❌ 프론트엔드에서는 직접 호출하지 않으며, 백엔드에서 Redirect해줌. ❌❌❌
    """
    access_token: str = getGoogleToken(code)
    user_profile: GoogleProfile = getGoogleUserName(access_token)

    # 처음 로그인한 유저이면 DB에 저장
    user = crud.get_user_by_oauth_id(dbSession, user_profile.id)
    if not user:
        user = crud.create_user(
            dbSession,
            UserCreate(
                name=user_profile.name,
                oauth_provider="google",
                oauth_id=user_profile.id,
            ),
        )

    # JWT 토큰 생성
    token = create_jwt_for_user(user)

    # 프론트엔드로 토큰 전달
    redirect_url = f"{settings.GOOGLE_ORIGIN_URI}?token={token}"
    return RedirectResponse(url=redirect_url, status_code=302)

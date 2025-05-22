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

router = APIRouter(tags=["auth"])


@router.get(
    "/auth/google/callback",
    status_code=status.HTTP_302_FOUND,
    response_class=RedirectResponse,
    responses={302: {"description": "로그인 후 프론트엔드로 리다이렉트"}},
)
def google_callback(
    request: Request, code: str, dbSession: Annotated[Session, Depends(get_db)]
):
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

    # 세션에 유저 정보 저장
    request.session["user"] = user.id

    # 프론트엔드로 리다이렉트
    return RedirectResponse(
        url=settings.GOOGLE_ORIGIN_URI,
        status_code=302,
    )

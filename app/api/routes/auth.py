from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.schemas import UserCreate
from app.utils.google_auth import getGoogleToken, getGoogleUserName
from app.utils.google_profile import GoogleProfile
from app.core.db import get_db
from app import crud

router = APIRouter(tags=["auth"])


@router.get("/auth/google/callback")
def google_callback(code: str, session: Annotated[Session, Depends(get_db)]):
    """
    Google 로그인 Callback
    프론트엔드에서는 직접 호출하지 않음.

    :param code: Google에서 받은 인증 코드
    """
    access_token: str = getGoogleToken(code)
    user_profile: GoogleProfile = getGoogleUserName(access_token)

    # 처음 로그인한 유저이면 DB에 저장
    user = crud.get_user_by_oauth_id(session, user_profile.id)
    if not user:
        user = crud.create_user(
            session,
            UserCreate(
                name=user_profile.name,
                oauth_provider="google",
                oauth_id=user_profile.id,
            ),
        )

    return {"message": "OK", "user_profile": user_profile}

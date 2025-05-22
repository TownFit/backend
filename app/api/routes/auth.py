from fastapi import APIRouter

from app.utils.google_auth import getGoogleToken, getGoogleUserName
from app.utils.google_profile import GoogleProfile


router = APIRouter(tags=["auth"])


@router.get("/auth/google/callback")
def google_callback(code: str):
    """
    Google 로그인 Callback
    프론트엔드에서는 직접 호출하지 않음.
    :param code: Google에서 받은 인증 코드
    """
    access_token: str = getGoogleToken(code)
    user_profile: GoogleProfile = getGoogleUserName(access_token)
    return {"message": "OK", "user_profile": user_profile}

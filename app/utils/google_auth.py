from fastapi import HTTPException
from app.core.config import settings
import requests

from app.utils.google_profile import GoogleProfile


# 구글 콜백 코드로부터 access token과 id token을 가져오는 함수
def getGoogleToken(code: str) -> str:
    endpoint = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code",
    }
    request = requests.post(endpoint, data=payload)

    if request.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get Google token")

    response = request.json()
    return response.get("access_token")


# 구글 access token으로부터 유저 정보를 가져오는 함수
def getGoogleUserName(accessToken: str) -> GoogleProfile:
    endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {accessToken}"}
    request = requests.get(endpoint, headers=headers)

    if request.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get Google user info")

    response = request.json()
    return GoogleProfile(id=response.get("sub"), name=response.get("name"))

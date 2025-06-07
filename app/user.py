from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.core.db import get_db
from app import crud
from app.core.config import settings
from datetime import datetime, timedelta, timezone


# JWT 인증 의존성
bearer_scheme = HTTPBearer(auto_error=True)


# 현재 로그인한 유저 조회 (JWT 기반)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    dbSession: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SESSION_SECRET_KEY,
            algorithms=["HS256"],
        )
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = crud.get_user(dbSession, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_jwt_for_user(user, expires_hours: int = 24) -> str:
    payload = {
        "user_id": user.id,
        "name": user.name,
        "oauth_provider": getattr(user, "oauth_provider", None),
        "exp": (datetime.now(timezone.utc) + timedelta(hours=expires_hours)),
    }
    token = jwt.encode(payload, settings.SESSION_SECRET_KEY, algorithm="HS256")
    return token

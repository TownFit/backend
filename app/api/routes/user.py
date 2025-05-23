from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import FacilityType, User, Recommendation
from app import crud


router = APIRouter(tags=["user"])


@router.get("/user/me", response_model=User)
def get_me(request: Request, dbSession: Annotated[Session, Depends(get_db)]) -> User:
    """
    현재 로그인한 유저의 정보 조회

    - 세션을 통해 로그인한 유저의 정보를 가져옴
    """
    if "user" not in request.session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 세션에서 유저 정보 가져오기
    user = crud.get_user(dbSession, request.session["user"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/user/get-recommendations", response_model=list[FacilityType])
def get_recommendations(
    request: Request, dbSession: Annotated[Session, Depends(get_db)]
) -> list[FacilityType]:
    """
    현재 로그인한 유저의 추천 시설타입 목록 조회

    - 세션을 통해 로그인한 유저의 정보를 가져옴
    """
    if "user" not in request.session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 세션에서 유저 정보 가져오기
    user = crud.get_user(dbSession, request.session["user"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 과거 설문조사에 따른 추천 시설타입 목록 조회
    recommendations = crud.get_recommendations(dbSession, user.id)
    result = list(map(lambda x: x.facility_type, recommendations))
    return result

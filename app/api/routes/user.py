from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import FacilityType, GeneralPostResponse, User, Recommendation
from app import crud
from app.user import get_current_user


router = APIRouter(tags=["user"])


@router.post("/user/logout", response_model=GeneralPostResponse)
def logout(
    request: Request,
    user: Annotated[User, Depends(get_current_user)],  # 검증용
) -> GeneralPostResponse:
    """
    로그아웃

    - 세션에서 유저 정보를 삭제
    """
    del request.session["user"]
    return GeneralPostResponse(message="success")


@router.get("/user/me", response_model=User)
def get_me(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    현재 로그인한 유저의 정보 조회

    - 세션을 통해 로그인한 유저의 정보를 가져옴
    """
    return user


@router.delete("/user/me", response_model=GeneralPostResponse)
def delete_me(
    request: Request,
    dbSession: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> GeneralPostResponse:
    """
    회원 탈퇴

    - 세션을 통해 로그인한 유저의 정보를 가져옴
    - 탈퇴시 유저 정보와 추천 시설타입 목록을 모두 삭제, 세션도 삭제
    """
    # 유저 정보 삭제
    crud.delete_recommendations(dbSession, user.id)
    crud.delete_user(dbSession, user.id)

    # 세션 삭제
    del request.session["user"]
    return GeneralPostResponse(message="success")


@router.get("/user/get-recommendations", response_model=list[FacilityType])
def get_recommendations(
    dbSession: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[FacilityType]:
    """
    현재 로그인한 유저의 추천 시설타입 목록 조회

    - 세션을 통해 로그인한 유저의 정보를 가져옴
    """
    # 과거 설문조사에 따른 추천 시설타입 목록 조회
    recommendations = crud.get_recommendations(dbSession, user.id)
    result = list(map(lambda x: x.facility_type, recommendations))
    return result

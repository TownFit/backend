from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.core.db import get_db
from app.schemas import (
    GeneralPostResponse,
    HasHistoryResponse,
    RecommendationCreate,
    SubmitSurveyRequest,
    User,
)
from app import crud
from app.core.config import logger
from app.utils import gemini
from app.user import get_current_user


router = APIRouter(tags=["survey"])


@router.get("/survey/has-history", response_model=HasHistoryResponse)
def has_history(
    dbSession: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> HasHistoryResponse:
    """
    현재 로그인한 유저가 과거 설문조사에 참여했는지 여부 조회

    - 세션을 통해 로그인한 유저의 정보를 가져옴
    """
    # 과거 설문조사(추천) 기록이 있는지 조회)
    recommendation = crud.has_recommendation(dbSession, user.id)
    return HasHistoryResponse(has_history=recommendation is not None)


@router.post("/survey/submit", response_model=GeneralPostResponse)
def submit_survey(
    body: SubmitSurveyRequest,
    dbSession: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> GeneralPostResponse:
    """
    설문조사 제출

    - 세션을 통해 로그인한 유저의 정보를 가져옴
    - 기존 설문조사 내역이 있으면, 삭제 후 새로운 추천 생성
    """
    # Gemini에 쿼리 날리기
    facilityTypes = crud.get_facility_types(dbSession)
    query = gemini.make_query(body, facilityTypes, number=3)
    response = json.loads(gemini.query_gemini(query))
    logger.info(f"Gemini response: {response}")

    # 기존 추천 기록 지우기 및 새로운 추천 기록 생성
    crud.delete_recommendations(dbSession, user.id)
    for facility_type_id in response:
        crud.create_recommendation(
            dbSession,
            RecommendationCreate(
                user_id=user.id,
                facility_type_id=facility_type_id,
            ),
        )

    return GeneralPostResponse(message="success")

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.model.coordinate import Coordinate
from app.schemas import User, AreaRecommendationResponse
from app import crud
from app.user import get_current_user
from app.utils.clustering import cluster_coordinates


router = APIRouter(tags=["map"])


@router.get("/map/get-recommendations", response_model=AreaRecommendationResponse)
def get_recommendations(
    dbSession: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],  # 검증용
) -> AreaRecommendationResponse:
    """
    추천 시설 조회

    - 현재 로그인한 유저의 추천 동네(영역)를 계산해 리턴합니다.
    """
    recommendations = crud.get_recommendations(dbSession, user.id)
    facilities = crud.get_facility_by_user_id(dbSession, user.id)
    coordinates = [Coordinate.from_facility(facility) for facility in facilities]
    areas = cluster_coordinates(coordinates, diversity_threshold=3, top_n=5)

    return AreaRecommendationResponse(
        recommendations=recommendations,
        areas=[area.to_schema() for area in areas],
    )

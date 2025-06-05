from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import asyncio

from app.core.db import get_db
from app.model.coordinate import Coordinate
from app.schemas import User, AreaRecommendationResponse
from app import crud
from app.user import get_current_user, bearer_scheme
from app.utils.clustering import cluster_coordinates_async
from app.utils.reverse_grocoding import reverse_geocode
from app.core.config import logger


router = APIRouter(tags=["map"], security=[bearer_scheme])


@router.get("/map/get-recommendations", response_model=AreaRecommendationResponse)
async def get_recommendations(
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
    areas = await cluster_coordinates_async(coordinates, diversity_threshold=3, top_n=5)
    schemas = [area.to_schema() for area in areas]

    # 역지오코딩 병렬 처리 및 fallback 적용
    async def safe_reverse_geocode(lat, lon):
        try:
            name = await reverse_geocode(lat, lon)
            return name
        except Exception as e:
            logger.exception(
                "Reverse geocoding failed for coordinates (%s, %s) : %s", lat, lon, e
            )
            return None

    tasks = [
        safe_reverse_geocode(schema.centroid.latitude, schema.centroid.longitude)
        for schema in schemas
    ]
    names = await asyncio.gather(*tasks)
    for schema, name in zip(schemas, names):
        schema.name = name

    return AreaRecommendationResponse(
        recommendations=recommendations,
        areas=schemas,
    )

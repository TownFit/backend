from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import (
    FacilityType,
    User,
)
from app import crud
from app.user import get_current_user


router = APIRouter(tags=["facility"])


@router.get("/facility/types", response_model=list[FacilityType])
def get_all_facility_types(
    dbSession: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[FacilityType]:
    """
    추천 가능한 모든 시설 타입 조회
    """
    facility_types = crud.get_facility_types(dbSession)
    return facility_types


@router.get("/facility/count", response_model=int)
def get_facility_count(
    dbSession: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> int:
    """
    전체 시설의 개수 조회
    """
    count = crud.get_facility_count(dbSession)
    return count

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# ---------------------
# Users Schemas
# ---------------------
class UserBase(BaseModel):
    name: str
    oauth_provider: str
    oauth_id: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------
# FacilityTypes Schemas
# ---------------------
class FacilityTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class FacilityTypeCreate(FacilityTypeBase):
    pass


class FacilityType(FacilityTypeBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------
# Facilities Schemas
# ---------------------
class FacilityBase(BaseModel):
    type_id: int
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float


class FacilityCreate(FacilityBase):
    pass


class Facility(FacilityBase):
    id: int
    facility_type: FacilityType

    class Config:
        from_attributes = True


# ---------------------
# Recommendations Schemas
# ---------------------
class RecommendationBase(BaseModel):
    user_id: int
    facility_id: int
    created_at: datetime
    description: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    pass


class Recommendation(RecommendationBase):
    id: int
    user: User
    facility: Facility

    class Config:
        from_attributes = True


# 관계 필드를 포함한 응답용 스키마
class UserWithRecommendations(User):
    recommendations: List[Recommendation] = []


class FacilityTypeWithFacilities(FacilityType):
    facilities: List[Facility] = []


class FacilityWithRecommendations(Facility):
    recommendations: List[Recommendation] = []


class RecommendationDetail(Recommendation):
    user: User
    facility: Facility

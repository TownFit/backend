from typing import Optional
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
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "홍길동",
                "oauth_provider": "google",
                "oauth_id": "1234567890",
            }
        }


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
        json_schema_extra = {
            "example": {"id": 1, "name": "헬스", "description": "헬스 관련 시설"}
        }


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
        json_schema_extra = {
            "example": {
                "id": 2,
                "type_id": 1,
                "name": "헬스장",
                "description": "24시간 운영",
                "latitude": 37.1234,
                "longitude": 127.5678,
                "facility_type": {
                    "id": 1,
                    "name": "헬스",
                    "description": "헬스 관련 시설",
                },
            }
        }


# ---------------------
# Recommendations Schemas
# ---------------------
class RecommendationBase(BaseModel):
    user_id: int
    facility_type_id: int
    created_at: datetime = datetime.now()
    description: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    pass


class Recommendation(RecommendationBase):
    id: int
    user: User
    facility_type: FacilityType

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "facility_type_id": 2,
                "created_at": "2024-05-22T12:00:00",
                "description": "추천 설명",
                "user": {
                    "id": 1,
                    "name": "홍길동",
                    "oauth_provider": "google",
                    "oauth_id": "1234567890",
                },
                "facility_type": {
                    "id": 2,
                    "name": "헬스",
                    "description": "헬스 관련 시설",
                },
            }
        }


# ---------------------
# For HTTP Requests
# ---------------------
class SubmitSurveyRequest(BaseModel):
    has_pet: bool
    has_child: bool
    has_student: bool
    has_elderly: bool
    notes: Optional[str] = None

    def __str__(self):
        return f"반려동물: {self.has_pet}, 어린이 동반 거주 여부: {self.has_child}, 학생 동반 거주 여부: {self.has_student}, 노인 동반 거주 여부: {self.has_elderly}, 비고: {self.notes if self.notes else '없음'}"


# ---------------------
# For HTTP Responses
# ---------------------
class HasHistoryResponse(BaseModel):
    has_history: bool

    class Config:
        json_schema_extra = {"has_history": True}


class GeneralPostResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {"message": "success"}

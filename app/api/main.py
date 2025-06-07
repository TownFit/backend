from fastapi import APIRouter

from app.api.routes import auth, user, survey, map, facility

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(survey.router)
api_router.include_router(map.router)
api_router.include_router(facility.router)

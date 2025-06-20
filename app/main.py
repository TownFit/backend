from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings

app = FastAPI(title="TownFit API")

# CORS 설정 (수정 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Set-Cookie",
        "Accept",
        "Origin",
        "User-Agent",
        "X-Requested-With",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Methods",
    ],
)

app.include_router(api_router)

from dotenv import load_dotenv
import logging
import os

load_dotenv()


class Settings:
    def __init__(self):
        self.CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
        self.DATABASE_URL = os.getenv("DATABASE_URL")

        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        self.GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        self.GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
        self.GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
        self.GOOGLE_ORIGIN_URI = os.getenv("GOOGLE_ORIGIN_URI")

        self.SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

from dotenv import load_dotenv
import logging
import os

load_dotenv()


class Settings:
    def __init__(self):
        self.CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
        self.DATABASE_URL = self._get_env_or_raise("DATABASE_URL")
        self.GEMINI_API_KEY = self._get_env_or_raise("GEMINI_API_KEY")

        self.GOOGLE_CLIENT_ID = self._get_env_or_raise("GOOGLE_CLIENT_ID")
        self.GOOGLE_CLIENT_SECRET = self._get_env_or_raise("GOOGLE_CLIENT_SECRET")
        self.GOOGLE_REDIRECT_URI = self._get_env_or_raise("GOOGLE_REDIRECT_URI")
        self.GOOGLE_ORIGIN_URI = self._get_env_or_raise("GOOGLE_ORIGIN_URI")

        self.NAVER_CLIENT_ID = self._get_env_or_raise("NAVER_CLIENT_ID")
        self.NAVER_CLIENT_SECRET = self._get_env_or_raise("NAVER_CLIENT_SECRET")

        self.SESSION_SECRET_KEY = self._get_env_or_raise("SESSION_SECRET_KEY")

    def _get_env_or_raise(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise RuntimeError(f"환경변수 '{key}'가 설정되어 있지 않습니다.")
        return value


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = Settings()

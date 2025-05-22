from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    def __init__(self):
        self.CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
        self.GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        self.GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
        self.GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


settings = Settings()

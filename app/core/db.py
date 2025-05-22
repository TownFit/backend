from sqlalchemy import Session, create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
session = Session(engine)
Base = declarative_base()

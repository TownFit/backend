from sqlalchemy.orm import Session

from . import models, schemas


# User
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Users(
        name=user.name,
        oauth_provider=user.oauth_provider,
        oauth_id=user.oauth_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_oauth_id(db: Session, oauth_id: str):
    return db.query(models.Users).filter(models.Users.oauth_id == oauth_id).first()


# Recommendation
def get_recommendations(db: Session, user_id: int):
    return (
        db.query(models.Recommendations)
        .filter(models.Recommendations.user_id == user_id)
        .all()
    )

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


def delete_user(db: Session, user_id: int):
    db.query(models.Users).filter(models.Users.id == user_id).delete()
    db.commit()


# Recommendation
def has_recommendation(db: Session, user_id: int):
    return (
        db.query(models.Recommendations)
        .filter(models.Recommendations.user_id == user_id)
        .first()
    )


def get_recommendations(db: Session, user_id: int):
    return (
        db.query(models.Recommendations)
        .filter(models.Recommendations.user_id == user_id)
        .all()
    )


def create_recommendation(db: Session, recommendation: schemas.Recommendation):
    db_recommendation = models.Recommendations(**recommendation.dict())
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation


def delete_recommendations(db: Session, user_id: int):
    db.query(models.Recommendations).filter(
        models.Recommendations.user_id == user_id
    ).delete()
    db.commit()


# FacilityTypes
def get_facility_types(db: Session):
    return db.query(models.FacilityTypes).all()


# Facility
def get_facility_by_user_id(db: Session, user_id: int):
    facilities = (
        db.query(models.Facilities)
        .join(
            models.Recommendations,
            models.Facilities.type_id == models.Recommendations.facility_type_id,
        )
        .filter(models.Recommendations.user_id == user_id)
        .all()
    )
    return facilities


def get_facility_count(db: Session):
    return db.query(models.Facilities).count()

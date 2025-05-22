from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    oauth_provider = Column(String)
    oauth_id = Column(String, unique=True)

    recommendations = relationship("Recommendations", back_populates="user")


class FacilityTypes(Base):
    __tablename__ = "facility_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)

    facilities = relationship("Facilities", back_populates="facility_type")


class Facilities(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("facility_types.id"))
    name = Column(String)
    description = Column(String, nullable=True)
    latitude = Column(Double)
    longitude = Column(Double)

    facility_type = relationship("FacilityTypes", back_populates="facilities")
    recommendations = relationship("Recommendations", back_populates="facility")


class Recommendations(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    created_at = Column(DateTime)
    description = Column(String, nullable=True)

    user = relationship("Users", back_populates="recommendations")
    facility = relationship("Facilities", back_populates="recommendations")

from __future__ import annotations
from app.schemas import Facility


class Coordinate:
    def __init__(self, latitude: float, longitude: float, type_id: int = -1):
        self.latitude = latitude
        self.longitude = longitude
        self.type_id = type_id

    @classmethod
    def from_facility(cls, facility: Facility) -> Coordinate:
        return cls(
            latitude=facility.latitude,
            longitude=facility.longitude,
            type_id=facility.type_id,
        )

    def to_list(self) -> list[float]:
        return [self.latitude, self.longitude]

    def __repr__(self) -> str:
        return f"Coordinate(latitude={self.latitude}, longitude={self.longitude}, type_id={self.type_id})"

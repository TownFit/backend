from __future__ import annotations
from app.schemas import Facility


class Coordinate:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def from_facility(cls, facility: Facility) -> Coordinate:
        return cls(latitude=facility.latitude, longitude=facility.longitude)

    def to_list(self) -> list[float]:
        return [self.latitude, self.longitude]

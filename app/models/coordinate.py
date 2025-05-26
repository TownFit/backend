from __future__ import annotations


class Coordinate:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def to_list(self) -> list[float]:
        return [self.latitude, self.longitude]

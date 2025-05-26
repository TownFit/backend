from app.models.coordinate import Coordinate
from __future__ import annotations


class Area:
    def __init__(self, centroid: Coordinate, range: float):
        self.centroid = centroid
        self.range = range

    @classmethod
    def from_coordinates(cls, coordinates: list[Coordinate]) -> Area:
        if not coordinates:
            raise ValueError("coordinates 리스트가 비어 있습니다.")

        avg_lat = sum(c.latitude for c in coordinates) / len(coordinates)
        avg_lon = sum(c.longitude for c in coordinates) / len(coordinates)
        centroid = Coordinate(avg_lat, avg_lon)

        radius = max(
            (
                (centroid.latitude - c.latitude) ** 2
                + (centroid.longitude - c.longitude) ** 2
            )
            ** 0.5
            for c in coordinates
        )
        return cls(centroid, radius)

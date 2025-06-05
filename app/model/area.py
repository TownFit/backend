from __future__ import annotations
from app.model.coordinate import Coordinate
from app import schemas


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

    def to_schema(self) -> schemas.Area:
        return schemas.Area(
            centroid=schemas.Coordinate(
                latitude=self.centroid.latitude,
                longitude=self.centroid.longitude,
            ),
            range=self.range * 100000,  # 위경도를 미터로 변환
        )

    def __repr__(self) -> str:
        return f"Area(centroid={self.centroid}, range={self.range})"

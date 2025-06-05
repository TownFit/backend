import unittest
from app.utils.clustering import cluster_coordinates
from app.model.coordinate import Coordinate
from app.model.area import Area


class TestClustering(unittest.TestCase):
    def setUp(self):
        # 테스트용 좌표 데이터 (type_id 다양성 포함, 예시 점 추가)
        self.coordinates = [
            Coordinate(latitude=37.1, longitude=127.1),  # type_id=1
            Coordinate(latitude=37.1001, longitude=127.1001),  # type_id=1
            Coordinate(latitude=37.2, longitude=127.2),  # type_id=2
            Coordinate(latitude=37.2001, longitude=127.2001),  # type_id=2
            Coordinate(latitude=37.3, longitude=127.3),  # type_id=3
            Coordinate(latitude=37.3001, longitude=127.3001),  # type_id=3
            Coordinate(latitude=37.4, longitude=127.4),  # type_id=1
            Coordinate(latitude=37.4001, longitude=127.4001),  # type_id=2
            Coordinate(latitude=37.5, longitude=127.5),  # type_id=3
            Coordinate(latitude=37.5001, longitude=127.5001),  # type_id=1
        ]
        # type_id를 임의로 부여하는 경우, Coordinate에 type_id 속성이 필요하다면 mock 객체로 대체
        for i, c in enumerate(self.coordinates):
            c.type_id = (i % 3) + 1

    def test_cluster_coordinates_basic(self):
        # diversity_threshold=2, top_n=2 등 기본 옵션으로 클러스터링
        areas = cluster_coordinates(
            self.coordinates,
            diversity_threshold=2,
            distance_threshold=0.001,
            min_range=0.0001,
            max_range=0.01,
            top_n=2,
        )
        self.assertIsInstance(areas, list)
        self.assertTrue(all(isinstance(a, Area) for a in areas))
        print(f"클러스터링 결과: {areas}")
        self.assertLessEqual(len(areas), 2)

    def test_cluster_coordinates_diversity(self):
        # diversity_threshold를 높게 설정하면 결과가 없을 수 있음
        areas = cluster_coordinates(
            self.coordinates,
            diversity_threshold=10,
            distance_threshold=0.001,
            min_range=0.0001,
            max_range=0.01,
            top_n=2,
        )
        self.assertEqual(len(areas), 0)


if __name__ == "__main__":
    unittest.main()

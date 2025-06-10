from app.model.area import Area
from app.model.coordinate import Coordinate
from collections import defaultdict
from sklearn.cluster import DBSCAN
from app.core.config import logger
import numpy as np
import asyncio


def cluster_coordinates(
    coordinates: list[Coordinate],
    diversity_threshold,
    distance_threshold: float = 0.00001 * 100,  # 약 100m
    min_range: float = 0.00001 * 300,  # 약 300m
    max_range: float = 0.00001 * 1000,  # 약 1000m
    top_n: int = 3,  # 상위 3개 Area만 반환
) -> list[Area]:
    """
    좌표 리스트를 공간적 근접성과 다양성 조건에 따라 여러 Area로 클러스터링합니다.

    인자:
        coordinates (list[Coordinate]): 클러스터링할 Coordinate 객체들의 리스트.
        diversity_threshold (int): 클러스터가 유효하려면 포함해야 하는 고유 type_id의 최소 개수.
        distance_threshold (float, optional): 클러스터 내 점들 사이의 최대 거리 (기본값: 0.00001 * 100, 약 100m).
        min_range (float, optional): Area의 최소 범위 (기본값: 0.00001 * 300, 약 300m).
        max_range (float, optional): Area의 최대 범위 (기본값: 0.00001 * 1000, 약 1000m).
        top_n (int, optional): 반환할 상위 클러스터(Area) 개수 (기본값: 3).

    반환값:
        list[Area]: 유효한 클러스터를 Area 객체로 변환한 리스트. 클러스터 크기(밀도) 기준 내림차순 정렬.

    참고:
        - DBSCAN 알고리즘을 사용하여 클러스터링합니다.
        - 고유 type_id가 diversity_threshold 이상인 클러스터만 유효합니다.
        - 각 Area의 range는 min_range와 max_range 사이로 제한됩니다.
    """
    # 좌표 추출
    coords = np.array([c.to_list() for c in coordinates])
    if len(coords) == 0:
        return []

    # DBSCAN으로 클러스터링
    db = DBSCAN(eps=distance_threshold, min_samples=diversity_threshold).fit(coords)
    labels = db.labels_
    logger.debug(
        "DBSCAN 클러스터링 완료, 레이블 수: %d",
        len(set(labels)) - (1 if -1 in labels else 0),
    )

    # 클러스터별로 시설과 type_id 집합을 동시에 관리
    clusters = defaultdict(lambda: {"coords": [], "type_ids": set()})
    for label, coord in zip(labels, coordinates):
        if label == -1:
            continue
        clusters[label]["coords"].append(coord)
        clusters[label]["type_ids"].add(getattr(coord, "type_id", None))

    # diversity 조건을 만족하는 클러스터만 추출
    valid_clusters = [
        cluster["coords"]
        for cluster in clusters.values()
        if len(cluster["type_ids"]) >= diversity_threshold
    ]
    logger.debug(
        "유효한 클러스터 수: %d (diversity_threshold=%d)",
        len(valid_clusters),
        diversity_threshold,
    )

    if not valid_clusters:
        return []

    # 개수(밀도) 기준 내림차순 정렬
    valid_clusters.sort(key=len, reverse=True)

    # Area 객체로 변환
    result = []
    max_len = len(valid_clusters[0])
    for index, coords in enumerate(valid_clusters):
        # 50 ~ 100으로 조절 후 순위 가중치 부여
        score = len(coords) / max_len * 100
        weighted_score = round((score / 2 + 50) * (0.9**index))

        area = Area.from_coordinates(coords, score=weighted_score)
        # Area의 range를 min_range와 max_range 사이로 제한
        if area.range < min_range:
            area.range = min_range
        elif area.range > max_range:
            area.range = max_range
        result.append(area)
    logger.debug(
        "Area 객체로 변환 완료, 총 Area 수: %d",
        len(result),
    )

    # 상위 N개 Area만 반환
    return result[:top_n]


async def cluster_coordinates_async_multi(
    coordinates: list[Coordinate],
    diversity_threshold,
    distance_thresholds: list[float] = [
        0.00001 * 50,
        0.00001 * 100,
        0.00001 * 200,
        0.00001 * 400,
    ],
    top_n: int = 3,
    min_range: float = 0.00001 * 500,
    max_range: float = 0.00001 * 1500,
) -> list[Area]:
    loop = asyncio.get_running_loop()

    def run_cluster(dt):
        return cluster_coordinates(
            coordinates,
            diversity_threshold,
            dt,
            min_range,
            max_range,
            top_n,
        )

    tasks = [loop.run_in_executor(None, run_cluster, dt) for dt in distance_thresholds]

    results = await asyncio.gather(*tasks)

    for res in results:
        if len(res) >= top_n:
            return res

    return results[0] if results else []

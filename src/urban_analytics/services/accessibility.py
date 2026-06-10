import geopandas as gpd
from loguru import logger

# Импортируем функции из ядра напрямую (благодаря настроенному __init__.py в core)
from urban_analytics.core import (
    calculate_accessibility_buffers,
    find_objects_within_buffers,
)


def evaluate_infrastructure_coverage(
    target_gdf: gpd.GeoDataFrame,
    infrastructure_gdf: gpd.GeoDataFrame,
    radius_meters: float,
) -> dict:
    """Оценивает покрытие целевых объектов зонами доступности инфраструктуры.

    Возвращает словарь с аналитическими метриками.
    """
    logger.info("Запуск комплексного сервиса оценки доступности.")

    # 1. Вызываем низкоуровневую логику создания буферов из ядра
    buffers_gdf = calculate_accessibility_buffers(infrastructure_gdf, radius_meters)

    # 2. Находим объекты, попавшие в эти зоны
    covered_objects_gdf = find_objects_within_buffers(target_gdf, buffers_gdf)

    # 3. Рассчитываем высокоуровневую аналитику (бизнес-логику)
    total_count = len(target_gdf)
    covered_count = len(covered_objects_gdf["geometry"].unique())

    coverage_share = (covered_count / total_count) * 100 if total_count > 0 else 0.0

    metrics = {
        "total_objects": total_count,
        "covered_objects": covered_count,
        "coverage_share_percent": round(coverage_share, 2),
    }

    logger.success(
        f"Анализ покрытия завершен. Обеспеченность: {metrics['coverage_share_percent']}%"
    )
    return metrics

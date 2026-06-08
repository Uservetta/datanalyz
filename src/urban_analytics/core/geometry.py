import geopandas as gpd
from loguru import logger

from urban_analytics.exceptions import CRSMismatchError, EmptyDataError


def calculate_accessibility_buffers(
    infrastructure_gdf: gpd.GeoDataFrame, radius_meters: float
) -> gpd.GeoDataFrame:
    """Создает зоны доступности (буферы) вокруг объектов инфраструктуры.

    infrastructure_gdf: GeoDataFrame с точками инфраструктуры.
    radius_meters: Радиус доступности в метрах.
    """
    logger.info(f"Запуск создания буферных зон радиусом {radius_meters} метров.")

    # Строгая проверка на пустые данные, как требует методичка
    if infrastructure_gdf.empty:
        logger.error("Передан пустой слой инфраструктуры.")
        raise EmptyDataError("Слой объектов инфраструктуры не содержит данных.")

    # Проверяем, что система координат (CRS) измеряется в метрах, а не в градусах
    if infrastructure_gdf.crs and infrastructure_gdf.crs.is_geographic:
        logger.warning(
            "Внимание: CRS использует географические градусы. Буфер в метрах может быть некорректным."
        )

    # Копируем данные и строим геометрический буфер
    gdf_buffered = infrastructure_gdf.copy()
    gdf_buffered["geometry"] = gdf_buffered.geometry.buffer(radius_meters)

    logger.success("Буферные зоны успешно построены.")
    return gdf_buffered


def find_objects_within_buffers(
    target_objects_gdf: gpd.GeoDataFrame, buffers_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Находит, какие целевые объекты попали в зону доступности буферов."""
    logger.info("Запуск пространственного анализа наложения слоев (Spatial Join).")

    if target_objects_gdf.empty or buffers_gdf.empty:
        raise EmptyDataError("Один из входных слоев для анализа наложения пуст.")

    # Проверяем совпадение систем координат с помощью нашего кастомного исключения
    if target_objects_gdf.crs != buffers_gdf.crs:
        logger.error(f"Несовпадение CRS: {target_objects_gdf.crs} и {buffers_gdf.crs}")
        raise CRSMismatchError(
            "Системы координат входных слоев должны полностью совпадать."
        )

    # Выполняем пространственное объединение (sjoin)
    # Оставляем только те объекты, которые пересеклись с буфером
    joined_gdf = gpd.sjoin(
        target_objects_gdf, buffers_gdf, how="inner", predicate="intersects"
    )

    logger.success(f"Анализ завершен. Найдено {len(joined_gdf)} точек пересечения.")
    return joined_gdf

import geopandas as gpd
from loguru import logger


def verify_site_suitability(area_hectares: float, power_megawatts: float) -> bool:
    """Проверяет пригодность промышленной площадки под требования ЦОД."""
    logger.info(
        f"Проверка параметров: Площадь={area_hectares} га, Мощность={power_megawatts} МВт"
    )

    min_area = 2.0  # Минимальная площадь в га для инфраструктуры ЦОД
    min_power = 10.0  # Минимальная подведенная мощность в МВт

    if area_hectares < min_area:
        logger.warning(f"Площадь участка меньше минимальной ({min_area} га)")
        return False
    if power_megawatts < min_power:
        logger.warning(f"Доступная мощность ниже нормы ({min_power} МВт)")
        return False

    logger.success("Участок пригоден для размещения ЦОД.")
    return True


def estimate_climatic_pue(average_temp: float) -> float:
    """Рассчитывает прогнозный климатический PUE (эффективность охлаждения) ЦОД."""
    base_pue = 1.2
    if average_temp > 0:
        thermal_load = (average_temp / 5.0) * 0.05
        predicted_pue = base_pue + thermal_load
    else:
        logger.info("Регион поддерживает технологию Free-cooling.")
        predicted_pue = base_pue

    return round(predicted_pue, 2)

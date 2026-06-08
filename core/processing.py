import numpy as np

def analyze_dc_urban_requirements(tier_level: int, dc_type: str, power_mw: float) -> dict:
    """
    Анализ градостроительных и инженерных требований к площадке ЦОД
    на основе отраслевых стандартов.
    
    tier_level: уровень надежности (1, 2, 3 или 4)
    dc_type: тип объекта ('commercial', 'corporate', 'state')
    power_mw: планируемая ИТ-нагрузка в МВт
    """
    if tier_level not in [1, 2, 3, 4]:
        raise ValueError("Уровень Tier должен быть целым числом от 1 до 4.")
    if power_mw <= 0:
        raise ValueError("Мощность должна быть строго больше нуля.")

    # 1. Анализ надежности и инженерных вводов (по материалам Server360)
    # Используем np.select для определения параметров Tier
    tier_conditions = [tier_level == 1, tier_level == 2, tier_level == 3, tier_level == 4]
    
    availability_options = [99.671, 99.741, 99.982, 99.995]
    downtime_options = ["28.8 часов", "22 часа", "1.6 часов", "26 минут"]
    power_inputs = [1, 1, 2, 2] # Количество независимых лучей питания от подстанции
    
    availability = float(np.select(tier_conditions, availability_options))
    max_downtime = str(np.select(tier_conditions, downtime_options))
    required_inputs = int(np.select(tier_conditions, power_inputs))

    # 2. Оценка площади участка и плотности застройки (урбанистический блок)
    # По бенчмаркам Softline/CBRE: коммерческим нужно меньше земли за счет модульности, 
    # государственным — больше из-за буферных зон безопасности периметра.
    if dc_type.lower() == 'commercial':
        area_multiplier = 0.15  # ~0.15 га на 1 МВт (высокая плотность)
        security_level = "Базовый периметр (КПП, видеонаблюдение)"
    elif dc_type.lower() == 'state':
        area_multiplier = 0.35  # ~0.35 га на 1 МВт (строгая безопасность, буферные зоны)
        security_level = "Высший уровень: 3 контура защиты, противотаранные барьеры"
    else: # corporate
        area_multiplier = 0.25  # среднее значение
        security_level = "Стандартный промышленный периметр безопасности"

    # Расчет рекомендуемой площади земельного участка (в гектарах)
    recommended_site_area = power_mw * area_multiplier

    return {
        "tier": f"Tier {tier_level}",
        "availability_pct": availability,
        "max_downtime_year": max_downtime,
        "required_power_inputs": required_inputs,
        "recommended_area_ha": float(np.round(recommended_site_area, 2)),
        "security_perimeter_req": security_level
    }
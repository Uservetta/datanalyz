from core.processing import analyze_dc_urban_requirements

def main():
    print("=== СИСТЕМА ГРАДОСТРОИТЕЛЬНОГО АНАЛИЗА ТЕРРИТОРИЙ ПОД ЦОД ===")
    
    # Задаем параметры для анализа концепции:
    target_tier = 3             # Самый частый промышленный уровень Tier III (из статьи)
    target_type = "commercial"  # Коммерческий дата-центр (Colocation)
    target_power = 24.0         # Мощность 24 МВт
    
    # Запуск расчетного модуля
    report = analyze_dc_urban_requirements(target_tier, target_type, target_power)
    
    # Вывод результатов для НИР
    print(f"\n[Входные параметры концепции]:")
    print(f" Назначение объекта: {target_type.upper()}")
    print(f" Планируемая ИТ-нагрузка: {target_power} МВт")
    
    print(f"\n[Инженерные требования (Server360 / Uptime Institute)]:")
    print(f"-> Класс надежности: {report['tier']}")
    print(f"-> Коэффициент отказоустойчивости: {report['availability_pct']}%")
    print(f"-> Допустимый простой в год: до {report['max_downtime_year']}")
    print(f"-> Мин. количество независимых лучей питания: {report['required_power_inputs']} входа")
    
    print(f"\n[Территориальные требования (Урбанистика & Безопасность)]:")
    print(f"-> Рекомендуемая площадь участка: {report['recommended_area_ha']} га")
    print(f"-> Требования к защите территории: {report['security_perimeter_req']}")

if __name__ == "__main__":
    main()
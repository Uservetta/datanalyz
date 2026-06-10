# Извлекаем высокоуровневые сервисы и кастомные ошибки
from urban_analytics.exceptions import (
    CRSMismatchError,
    EmptyDataError,
    UrbanAnalyticsError,
)
from urban_analytics.services import evaluate_infrastructure_coverage

# Переменная __all__ строго определяет, что именно станет доступно пользователю при импорте библиотеки.
__all__ = [
    "evaluate_infrastructure_coverage",
    "UrbanAnalyticsError",
    "EmptyDataError",
    "CRSMismatchError",
]

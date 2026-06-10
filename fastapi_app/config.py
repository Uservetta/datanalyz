from pydantic import BaseModel
from typing import List

# 1. Кастомный класс для статической конфигурации (Startup)
class AppConfig:
    def __init__(self):
        self.app_name: str = "Laboratory FastAPI App"
        self.app_version: str = "1.0.0"
        self.app_description: str = "Учебное приложение"
        self.app_authors: List[str] = ["Uservetta"]

    def get_meta(self) -> dict:
        """Возвращает метаданные для инициализации FastAPI"""
        return {
            "title": self.app_name,
            "version": self.app_version,
            "description": self.app_description
        }

# Инициализируем статическую конфигурацию ОДИН раз при старте
static_config = AppConfig()


# 2. Модель Pydantic для валидации динамических параметров (Runtime)
class RuntimeSettings(BaseModel):
    log_level: str = "INFO"
    feature_flag: bool = False
    maintenance_mode: bool = False
    runtime_message: str = "Базовый режим работы"

# Храним динамические настройки в памяти как один разделяемый объект
runtime_config = RuntimeSettings()
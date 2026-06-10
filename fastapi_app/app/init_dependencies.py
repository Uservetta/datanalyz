from app.common.config import AppConfig, RuntimeConfigModel
from app.schemas.app_config import AppConfigModel
from app.services.runtime_config_service import RuntimeConfigService

# Наш кастомный DI-контейнер (словарь)
_container = {}

def init_dependencies() -> dict:
    global _container
    
    # 1. Загружаем статику
    raw_config = AppConfig()
    app_config = AppConfigModel(
        app_name=raw_config.app_name,
        app_version=raw_config.app_version,
        app_description=raw_config.app_description,
        app_authors=raw_config.app_authors
    )
    
    # 2. Инициализируем дефолтный runtime-синглтон и сервис
    runtime_model = RuntimeConfigModel()
    runtime_service = RuntimeConfigService(initial_config=runtime_model)
    
    # 3. Складываем в контейнер
    _container["app_config"] = app_config
    _container["runtime_config_service"] = runtime_service
    
    return _container

def get_container() -> dict:
    """Вспомогательная функция для доступа к синглтону контейнера"""
    return _container
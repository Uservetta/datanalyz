from fastapi import APIRouter
from config import static_config, runtime_config, RuntimeSettings

router = APIRouter()

# 1. Проверка работоспособности
@router.get("/health")
async def health_check():
    return {"status": "ok"}

# 2. Получение статической конфигурации
@router.get("/config/app")
async def get_static_config():
    return {
        "app_name": static_config.app_name,
        "app_version": static_config.app_version,
        "app_description": static_config.app_description,
        "app_authors": static_config.app_authors
    }

# 3. Получение динамических параметров
@router.get("/config/runtime")
async def get_runtime_config():
    return runtime_config

# 4. Обновление динамических параметров в памяти приложения
@router.put("/config/runtime")
async def update_runtime_config(new_settings: RuntimeSettings):
    global runtime_config
    # Обновляем поля нашего singleton-объекта
    runtime_config.log_level = new_settings.log_level
    runtime_config.feature_flag = new_settings.feature_flag
    runtime_config.maintenance_mode = new_settings.maintenance_mode
    runtime_config.runtime_message = new_settings.runtime_message
    
    return {"message": "Runtime конфигурация успешно обновлена", "current": runtime_config}
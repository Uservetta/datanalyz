from fastapi import APIRouter, Depends
from app.schemas.responses import HealthResponse
from app.schemas.app_config import AppConfigModel
from app.common.config import RuntimeConfigModel
from app.schemas.runtime_config import RuntimeConfigUpdateModel
from app.dependencies import get_app_config, get_runtime_config_service

router = APIRouter(tags=["configuration"])

# 1. Проверка работоспособности
@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}

# 2. Получение статической конфигурации
@router.get("/config/app", response_model=AppConfigModel)
def get_static_config(config=Depends(get_app_config)):
    return config

# 3. Получение динамической конфигурации
@router.get("/config/runtime", response_model=RuntimeConfigModel)
def get_runtime_config(service=Depends(get_runtime_config_service)):
    return service.get_config()

# 4. Обновление динамической конфигурации
@router.put("/config/runtime", response_model=RuntimeConfigModel)
def update_runtime_config(new_settings: RuntimeConfigUpdateModel, service=Depends(get_runtime_config_service)):
    return service.update_config(new_settings)
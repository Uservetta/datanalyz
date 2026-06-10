from pydantic import BaseModel, Field
from typing import Literal

class RuntimeConfigUpdateModel(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(..., description="Уровень логирования")
    feature_flag: bool = Field(..., description="Флаг новой фичи")
    maintenance_mode: bool = Field(..., description="Режим тех. обслуживания")
    runtime_message: str = Field(..., description="Сообщение статуса")
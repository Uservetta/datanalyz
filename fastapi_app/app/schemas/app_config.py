from pydantic import BaseModel, Field
from typing import List

class AppConfigModel(BaseModel):
    app_name: str = Field(..., description="Название приложения")
    app_version: str = Field(..., description="Версия")
    app_description: str = Field(..., description="Описание")
    app_authors: List[str] = Field(..., description="Авторы проекта")
from pydantic import BaseModel

class AppConfig:
    def __init__(self):
        self.app_name = "Laboratory FastAPI App"
        self.app_version = "1.0.0"
        self.app_description = "Учебное приложение на FastAPI"
        self.app_authors = ["Лиза"]

class RuntimeConfigModel(BaseModel):
    log_level: str = "INFO"
    feature_flag: bool = False
    maintenance_mode: bool = False
    runtime_message: str = "Приложение работает в штатном режиме"
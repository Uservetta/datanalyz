from typing import Generator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

class Settings(BaseSettings):
    # Автоматически подтянет значение DATABASE_URL из .env или окружения
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()

# Создаем движок SQLAlchemy с проверкой активности пула соединений
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Фабрика для генерации сессий
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Базовый класс для декларативных ORM-моделей
class Base(DeclarativeBase):
    pass

# Зависимость (Dependency) для получения сессии БД в эндпоинтах FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
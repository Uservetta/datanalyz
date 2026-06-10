import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.init_dependencies import init_dependencies
from app.routes.config import router as config_router
#импорт для 8лабы
from app.territories.router import router as territories_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # На этапе старта приложения инициализируем наш словарь зависимостей
    deps = init_dependencies()
    print("Dependencies initialized:", deps)
    yield
    print("App is shut down")

# Создаем приложение и передаем статические метаданные
app = FastAPI(
    lifespan=lifespan,
    title=os.environ.get("APP_NAME", "Urban Territories CRUD Service (Lab 8)"),
    description=os.environ.get("APP_DESCRIPTION", "Учебное приложение с Pydantic, DI и поддержкой PostGIS"),
    version=os.environ.get("APP_VERSION", "3.0.0")
)

# Редирект с корня на документацию
@app.get("/", include_in_schema=False)
async def get_root():
    return RedirectResponse("/docs")

# --- ПОДКЛЮЧАЕМ РОУТЕРЫ К ПРИЛОЖЕНИЮ ---

# Старый роутер из прошлых лаб
app.include_router(config_router)

# Новый роутер территорий и пространственных данных
app.include_router(territories_router)
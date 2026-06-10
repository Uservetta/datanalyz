import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.init_dependencies import init_dependencies
from app.routes.config import router as config_router

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
    title=os.environ.get("APP_NAME", "Laboratory FastAPI App v6"),
    description=os.environ.get("APP_DESCRIPTION", "Учебное приложение с Pydantic и DI"),
    version=os.environ.get("APP_VERSION", "2.0.0")
)

# Редирект с корня на документацию
@app.get("/", include_in_schema=False)
async def get_root():
    return RedirectResponse("/docs")

# ПОДКЛЮЧАЕМ РОУТЕР К ПРИЛОЖЕНИЮ, ЧТОБЫ ОН ПОЯВИЛСЯ В SWAGGER
app.include_router(config_router)
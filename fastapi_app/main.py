from fastapi import FastAPI
from config import static_config
from routes import router

# Инициализируем FastAPI, используя данные кастомного класса конфигурации
app = FastAPI(**static_config.get_meta())

# Подключаем наши маршруты
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # Запуск сервера на локальном хосте
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
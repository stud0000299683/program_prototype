from fastapi import FastAPI
from university_router import router

app = FastAPI()

# Подключаем роутер к приложению
app.include_router(router)

# Точка входа в приложение
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

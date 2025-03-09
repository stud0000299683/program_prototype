from fastapi import FastAPI
from university_router import router as ur_router
import university_router
from auth_router import router as auth_router


app = FastAPI()


# Подключаем роутер к приложению
# app.include_router(router)
app.include_router(auth_router)
app.include_router(ur_router)


# Точка входа в приложение
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, HTTPException
import uvicorn
import re

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "OK"}


# проводит операцию сложения
@app.post("/addition")
async def add(a: int = 0, b: int = 0):
    return {"Сложение": a + b}


# проводит операцию вычитания
@app.get("/subtraction")
async def summ(a: int = 0, b: int = 0):
    return {"Вычитание": a-b}


# проводит операцию умножения
@app.get("/multiply")
async def summ(a: int = 0, b: int = 0):
    return {"Умножение": a*b}


# проводит операцию деления
@app.get("/division")
async def summ(a: int = 0, b: int = 0):
    if b == 0:
        raise HTTPException(status_code=400, detail="Деление на 0")
    return {"Деление": a/b}


# создает простое выражения
@app.post("/create_operation")
async def create_operation(first: int, operation: str, second: int):
    OPERATIONS = {"+", "-", "*", "/"}
    if operation not in OPERATIONS:
        raise  HTTPException(status_code=400, detail="Неправильный тип операции")
    expression = f"({first}{operation}{second})"
    return {"выражение": expression}


@app.post("/create_full_operation")
async def create_full_operation(full: str):
    full = full.replace(" ", "")
    pattern = r"^[\d+\-*/()]+$"
    if bool(re.match(pattern, full)):
        try:
            result = eval(full)
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail='есть запрещенные символы')


if __name__ == "__main__":
    uvicorn.run("calc:app", host="0.0.0.0", port=8000, reload=True)

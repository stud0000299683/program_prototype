from fastapi import FastAPI
import uvicorn
from pydantic_lection_file2 import Student

app = FastAPI()

LANG = {
    1: "C#",
    2: "c++",
    3: "py"
}

@app.get("/")
async def root():
    return {"mes": "Hello word"}


@app.get("/lang/{item_id}")
async def lang(item_id):
    return {"lang": LANG.get(int(item_id), "unknown")}


@app.get("/sum/")
async def summ(a: int = 0, b: int = 0):
    return {"sum": a+b}


@app.post("/student")
async def student(model: Student):
    return model.model_dump()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

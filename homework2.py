
from typing import Literal, List
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr, EmailStr, Field
import json
from datetime import date
import os

app = FastAPI()

'''
Создайте сервис для сбора обращения абонентов на основе FastAPI.
Эндпойнт должен принимать следующие атрибуты:

 фамилия – с заглавной буквы, содержит только кирилицу;
 имя – с заглавной буквы, содержит только кирилицу;
 дату рождения;
 номер телефона;
 e-mail.
Все переданные атрибуты должны валидироваться с помощью модели Pydantic.
Результат сохраняется на диске в виде json-файла, содержащего переданные атрибуты.

Добавьте в сервис следующие атрибуты:

 причина обращения – нет доступа к сети, не работает телефон, не приходят письма;
 дата и время обнаружения проблемы.
Все переданные атрибуты должны валидироваться с помощью модели Pydantic.


'''

# Модель Pydantic для валидации


class RequestReason(BaseModel):
    reason: Literal['нет доступа к сети', 'не работает телефон', 'не приходят письма']
    detection_time: str  # Дата и время обнаружения проблемы в формате ISO 8601


class Person(BaseModel):
    surname: str = Field(pattern=r'^[А-ЯЁ][а-яё]+$')   # Фамилия с заглавной буквы, только кириллица
    name: str = Field(pattern=r'^[А-ЯЁ][а-яё]+$')   # Имя с заглавной буквы, только кириллица
    birth_date: date = Field(default="2000-01-01", title="birthday day")
    phone_number: str = Field(pattern=r'^\+?\d{10,15}$')  # Номер телефона (пример: +79991234567)
    email: EmailStr  # E-mail


class Subscriber(Person):
    reasons: List[RequestReason]  # Список причин обращения


# Эндпойнт для сбора обращений
@app.post("/submit/")
async def submit_request(subscriber: Subscriber):
    data = subscriber.dict()
    data['birth_date'] = subscriber.birth_date.isoformat()
    file_path = "subscribers.json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
            existing_data.append(data)
    else:
        existing_data = [data]

    with open(file_path, "w",  encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

    return {"message": "Обращение успешно сохранено", "data": data}

if __name__ == "__main__":
    uvicorn.run("homework2:app", host="0.0.0.0", port=8000, reload=True)

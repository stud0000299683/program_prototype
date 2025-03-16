from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Инициализация клиента для тестов
from hw3.main import app

client = TestClient(app)


def test_read_faculties_success(client):
    response = client.get("/university/faculties/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)


def test_read_faculties_cache(client, redis_client):
    redis_client.set("faculties", '[{"id": 1, "name": "Факультет A"}]')
    response = client.get("/university/faculties/")
    assert response.status_code == 200
    assert response.json()["data"] == [{"id": 1, "name": "Факультет A"}]


def test_create_faculty_success(client):
    payload = {"id": 1, "name": "Факультет B"}
    response = client.post("/university/faculties/", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Факультет создан"


def test_create_faculty_duplicate(client):
    payload = {"id": 1, "name": "Факультет B"}
    client.post("/university/faculties/", json=payload)  # Создаем первый раз
    response = client.post("/university/faculties/", json=payload)  # Пытаемся создать повторно
    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_create_student_success(client):
    payload = {"id": 1, "faculty_id": 1, "course_id": 1}
    response = client.post("/university/students/", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Студент создан"


def test_create_student_invalid_faculty(client):
    payload = {"id": 1, "faculty_id": -1, "course_id": 1}  # Несуществующий faculty_id
    response = client.post("/university/students/", json=payload)
    assert response.status_code == 400
    assert "Факультет не найден" in response.json()["detail"]


def test_read_grades_success(client):
    response = client.get("/university/grades/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for grade in response.json():
        assert "subject" in grade and "score" in grade and "student_id" in grade


def test_read_grades_empty(client):
    # Убедимся, что таблица оценок пуста (например, через фикстуру)
    response = client.get("/university/grades/")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_login_success(client):
    payload = {"username": "test@example.com", "password": "password123"}
    response = client.post("/auth/login", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    payload = {"username": "wrong@example.com", "password": "wrongpassword"}
    response = client.post("/auth/login", data=payload)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]



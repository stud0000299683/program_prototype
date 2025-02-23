from datetime import date
from pydantic import BaseModel, field_validator, model_validator, Field, EmailStr


class Person(BaseModel):
    id: int = Field(default=1, description="unique id", )
    name: str = Field(default="first_name_last_name", min_length=3, max_length=100)
    b_date: date = Field(default="2000-01-01", title="birthday day")
    email: EmailStr


class Student(Person):
    score: int = Field(default=80, ge=80, le=300)


class Postgraduate(Person):
    grant: int = Field(ge=1000, le=10000)


if __name__ == "__main__":
    alina = Student(score=81, email="eml")
    print(alina)

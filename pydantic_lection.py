from datetime import date
from pydantic import BaseModel, field_validator, model_validator


class Student(BaseModel):
    id: int
    name: str
    b_date: date

    @field_validator("name", mode="before")
    def validate_name(cls, v):
        if isinstance(v, str):
            return v
        elif isinstance(v, int):
            return str(v)
        else:
            raise ValueError("name must be str")


    @model_validator(mode="after")
    def validate_age(self):
        today = date.today()
        age = today.year - self.b_date.year - ((today.month, today.day) < (self.b_date.month, self.b_date.day))

        if age < 18:
            raise ValueError("user must be over 18")
        elif age > 118:
            raise ValueError("user must be under 18")
        else:
            return self

    @model_validator(mode="after")
    def validate_nname(self):
        if self.name.strip() == "":
            self.name = f"User_{self.id}"
        else:
            return self


if __name__ == "__main__":
    petr = Student(
        id=1,
        name="Petr",
        b_date=date(year=2003, month=5, day=6)
    )

    # print(petr)
    # print(petr.model_dump())
    # print(type(petr.model_dump()))
    # print(petr.model_dump_json())
    # print(type(petr.model_dump_json()))

    oleg_dict = {"id": 2,
                 "name": "",
                 "b_date": "2000-01-01"
    }

    oleg = Student(**oleg_dict)
    print(oleg.model_dump())

from datetime import date
from pydantic import BaseModel, field_validator, model_validator, Field, EmailStr
from typing_extensions import Annotated


class CarProperty(BaseModel):
    id: int = Field(default=1, description="unique id")
    name: str = Field(default="auto")
    value: str = Field(default="auto")

class Car(BaseModel):
    id: Annotated[int, Field(default=1, description="unique id")]
    brand: str = Field(default="auto")
    properties: list[CarProperty]


if __name__ == "__main__":
    p1 = CarProperty(id=1, name="max_speed", value="200")
    p2 = CarProperty(id=2, name="color", value="black")
    p3 = CarProperty(id=3, name="clereance", value="220")

    myCar = Car(id=1, brand="Toyota", properties=[p1, p2, p3])
    print(myCar.model_dump())

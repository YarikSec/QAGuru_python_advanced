from datetime import datetime

from pydantic import BaseModel, field_validator
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    birth_date: str
    products: list['Product'] = Relationship(back_populates="user")


class UserCreate(BaseModel):
    name: str
    surname: str
    birth_date: str
    products: list['Product']

    @field_validator('birth_date')
    def validate_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return value
        except ValueError:
            raise ValueError('Дата должна быть в формате дд.мм.гггг')


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    birth_date: str | None = None
    products: list['Product'] = []

    @field_validator('birth_date')
    def validate_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return value
        except ValueError:
            raise ValueError('Дата должна быть в формате дд.мм.гггг')


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    price: float
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="products")
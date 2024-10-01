from datetime import datetime
from enum import Enum
from typing import TypeVar

from sqlalchemy import BigInteger
from sqlmodel import Field, SQLModel, select
from src.models.base import BaseModel, table_prefix
from src.routes.deps.db_session import DBSession


class GenderType(str, Enum):
    male = "male"
    female = "female"


class DisabilityType(str, Enum):
    none = "none"
    first_degree = "first_degree"
    second_degree = "second_degree"
    third_degree = "third_degree"
    forth_degree = "forth_degree"


class DisabilityState(str, Enum):
    physical = "physical"
    mental = "mental"
    vision = "vision"
    hearing = "hearing"
    psychological = "psychological"
    parent = "parent"
    other = "other"
    aids = "aids"


class Region(str, Enum):
    R0 = "Toshkent shahar"
    R1 = "Andijon viloyati"
    R2 = "Buxoro viloyati"
    R3 = "Farg'ona viloyati"
    R4 = "Jizzax viloyati"
    R5 = "Xorazm viloyati"
    R6 = "Namangan viloyati"
    R7 = "Navoiy viloyati"
    R8 = "Qashqadaryo viloyati"
    R9 = "Qoraqalpog‘iston Respublikasi"
    R10 = "Samarqand viloyati"
    R11 = "Sirdaryo viloyati"
    R12 = "Surxondaryo viloyati"
    R13 = "Toshkent viloyati"


UserType = TypeVar("UserType", bound="User")


class User(BaseModel, table=True):
    __tablename__ = table_prefix + "users"

    user_id: int = Field(sa_type=BigInteger, unique=True)
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    birth_year: int | None = None
    phone: str | None = None
    gender: GenderType | None = None
    disability_type: DisabilityType | None = None
    disability_state: DisabilityState | None = None
    region: Region | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    @staticmethod
    def get_by_user_id(user_id: int, session: DBSession) -> UserType | None:
        statement = select(User).where(User.user_id == user_id)
        return session.exec(statement).first()

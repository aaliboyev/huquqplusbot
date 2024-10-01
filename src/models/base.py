from typing import Type
from sqlmodel import Field, SQLModel, select
from src.routes.deps.db_session import DBSession

table_prefix = "tg_bot_"


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    metadata = SQLModel.metadata

    @classmethod
    def get_by_id(cls: Type[SQLModel], id: int, session: DBSession) -> SQLModel | None:
        statement = select(cls).where(cls.id == id)
        return session.exec(statement).first()

from fastapi import Depends
from src.database.mysql import engine
from collections.abc import Generator
from typing import Annotated
from sqlmodel import Session


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_db)]

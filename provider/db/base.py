import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, create_engine, Field, Session

sqlite_file_name = "file_server.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)


class BaseFileInfo(BaseModel):
    file_uid: str = Field(index=True)
    file_hash: str = Field()
    file_path: str = Field()


class BaseFileToken(BaseModel):
    file_uid: str = Field(index=True)
    token: str = Field(index=True)
    expiry: Optional[datetime] = Field()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

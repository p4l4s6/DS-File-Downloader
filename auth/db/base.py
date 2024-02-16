import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, create_engine, Field, Session
from sqlalchemy import Column, DateTime, func, Enum

from . import constants

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)


class BaseUser(BaseModel):
    name: str = Field(index=True, max_length=30)
    email: str = Field(index=True, unique=True, max_length=50)
    role: str = Field(sa_column=Column(Enum(constants.UserRole), default=constants.UserRole.USER))
    is_active: bool = Field(default=True)


class BaseFileInfo(BaseModel):
    name: str = Field(max_length=30)
    file_uid: uuid.UUID = Field(index=True)
    file_hash: str = Field()
    file_size: str = Field()


class BaseFileLocation(BaseModel):
    server_ip: str = Field()
    file_path: str = Field()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

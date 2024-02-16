import uuid
from datetime import datetime
from typing import List

from passlib.context import CryptContext
from sqlmodel import Field, Relationship

from .base import BaseModel, BaseUser, BaseFileInfo, BaseFileLocation

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class User(BaseUser, table=True):
    hashed_password: str = Field()

    tokens: List["AuthToken"] = Relationship(back_populates="user")

    def save_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def varify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)


class AuthToken(BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(index=True, max_length=30)
    expiry: datetime = Field()
    user: User = Relationship(back_populates="tokens")


class FileInfo(BaseFileInfo, table=True):
    locations: List["FileLocation"] = Relationship(back_populates="fileinfo")


class FileLocation(BaseFileLocation, table=True):
    fileinfo_id: int = Field(foreign_key="fileinfo.id")
    fileinfo: FileInfo = Relationship(back_populates="locations")

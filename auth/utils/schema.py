import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel
from db.base import BaseUser, BaseFileInfo, BaseFileLocation


class LoginSchema(SQLModel):
    email: str
    password: str


class LoginResponseSchema(BaseUser):
    token: Optional[str] = None
    expiry: Optional[datetime] = None


class FileResponseSchema(BaseFileInfo):
    token: Optional[str] = None
    locations: List[BaseFileLocation] = None

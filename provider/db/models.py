import uuid
from datetime import datetime
from typing import List
from sqlmodel import Field, Relationship

from .base import BaseModel, BaseFileInfo, BaseFileToken


class FileInfo(BaseFileInfo, table=True):
    tokens: List["FileToken"] = Relationship(back_populates="fileinfo")


class FileToken(BaseFileToken, table=True):
    file_id: int = Field(foreign_key="fileinfo.id")
    fileinfo: FileInfo = Relationship(back_populates="tokens")

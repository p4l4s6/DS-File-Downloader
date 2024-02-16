import datetime
import uuid

from sqlmodel import Session, select

from . import models


# file related operation
def get_file_by_id(session: Session, file_id: int):
    return session.get(models.FileInfo, file_id)


def get_file_by_uuid(session: Session, file_uid: str):
    return session.exec(select(models.FileInfo).where(models.FileInfo.file_uid == file_uid)).first()


def get_filetoken_by_token(session: Session, token_str: str, file_uid: str):
    return session.exec(select(models.FileToken).where(
        models.FileToken.token == token_str,
        models.FileToken.file_uid == file_uid,
        models.FileToken.expiry > datetime.datetime.utcnow()
    )).first()


# Token related operation
def add_token(session: Session, file_uid: str, token: str):
    file_info = get_file_by_uuid(session, file_uid)
    if file_info:
        file_token = models.FileToken(
            file_id=file_info.id,
            file_uid=file_uid,
            token=token,
            expiry=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        session.add(file_token)
        session.commit()
        # session.refresh(file_token)

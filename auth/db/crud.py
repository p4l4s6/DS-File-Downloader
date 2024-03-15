import datetime
import uuid

from sqlmodel import Session, select

from . import models


# User related operation
def get_user(session: Session, user_id: int):
    return session.get(models.User, user_id)


def get_auth_token_by_token(session: Session, token_str: str):
    return session.exec(select(models.AuthToken).where(models.AuthToken.token == token_str)).first()


def get_user_by_email(session: Session, email: str):
    return session.exec(select(models.User).where(models.User.email == email)).first()


# Token related operation
def add_token(session: Session, user_id: int):
    token = session.exec(select(models.AuthToken).where(
        models.AuthToken.user_id == user_id, models.AuthToken.expiry > datetime.datetime.utcnow()
    )).first()
    if not token:
        token = models.AuthToken(
            user_id=user_id,
            token=uuid.UUID(str(uuid.uuid4())).hex,
            expiry=datetime.datetime.utcnow() + datetime.timedelta(days=14)
        )
        session.add(token)
        session.commit()
        session.refresh(token)
    return token


# file related operation
def get_files_list(session: Session):
    return session.exec(select(models.FileInfo)).all()


def get_file_by_id(session: Session, file_id: int):
    return session.get(models.FileInfo, file_id)


def get_file_by_uuid(session: Session, file_uid: uuid.UUID):
    return session.exec(select(models.FileInfo).where(models.FileInfo.file_uid == file_uid)).first()

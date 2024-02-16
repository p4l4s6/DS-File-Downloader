import uuid

from sqlalchemy.orm import Session

from . import models
from .constants import UserRole


def create_user(session: Session):
    db_user = models.User(
        name='Mr. Admin', email="admin@admin.com",
        hashed_password="1234", role=UserRole.ADMIN
    )
    db_user.save_password("1234")
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def generate_file_info(session: Session):
    for i in range(0, 100):
        file_info = models.FileInfo(
            id=i,
            name=f"File {i}",
            file_uid=uuid.uuid4(),
            file_size="18 MB",
            file_hash="D6617A009C0C6C9AEBF7398D43CAD6D1985DDC1B9AB0479E2EA977362B8AF5B0"
        )
        session.add(file_info)
        for j in range(1, 4):
            location = models.FileLocation(
                fileinfo_id=i,
                server_ip=f"server{j}",
                file_path="/files/file_example.mp4"
            )
            session.add(location)
    session.commit()

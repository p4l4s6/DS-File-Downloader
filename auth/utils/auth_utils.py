from typing import Optional

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import crud, models
from db.base import get_session, BaseUser


class CustomContext:
    def __init__(self, user: models.BaseUser, session: Session):
        self.user = user
        self.session = session


async def get_token(request: Request):
    authorization: Optional[str] = request.headers.get("Authorization")
    scheme, token = authorization.split() if authorization else (None, None)
    if scheme and scheme.lower() != "token":
        return None
    return token


async def verify_token(session, token_str):
    if not token_str:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = crud.get_auth_token_by_token(session, token_str)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token.user


async def get_current_user(session: Session = Depends(get_session), token_str=Depends(get_token), ) -> CustomContext:
    user = await verify_token(session, token_str)
    return CustomContext(BaseUser.from_orm(user), session)

import uuid
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import parse_obj_as
from sqlmodel import Session
from db import base, crud
from utils import schema, broker_utils, auth_utils

app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     base.create_db_and_tables()


@app.get("/")
async def root(session: Session = Depends(base.get_session)):
    # helper.create_user(session)
    # helper.generate_file_info(session)
    return {"message": "Hello World"}


@app.post("/auth/login/")
async def login(
        data: schema.LoginSchema,
        session: Session = Depends(base.get_session)
) -> schema.LoginResponseSchema:
    user = crud.get_user_by_email(session, data.email)
    if user and user.varify_password(data.password):
        token = crud.add_token(session, user.id)
        response = schema.LoginResponseSchema(**token.user.dict())
        response.token = token.token
        response.expiry = token.expiry
        return response
    raise HTTPException(status_code=400, detail="Invalid credentials")


@app.get("/file/")
async def get_files(
        session: Session = Depends(base.get_session)
) -> list[base.BaseFileInfo]:
    file_list = crud.get_files_list(session)
    return file_list
    # return parse_obj_as(List[base.BaseFileInfo], file_list)


@app.get("/file/{file_id}/")
async def get_file_detail(
        file_id: int,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> schema.FileResponseSchema:
    file_info = crud.get_file_by_id(context.session, file_id)
    if file_info:
        download_token = str(uuid.uuid4())
        broker_utils.publish_event({
            "file_uid": str(file_info.file_uid),
            "token": download_token
        })
        response = schema.FileResponseSchema(**file_info.dict())
        response.locations = file_info.locations
        response.token = download_token
        return response
    raise HTTPException(status_code=404, detail="File not found")

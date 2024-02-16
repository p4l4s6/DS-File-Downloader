import os
import threading

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from db import crud, base
from utils import broker_utils

app = FastAPI()


@app.on_event("startup")
def on_startup():
    base.create_db_and_tables()
    consumer_thread = threading.Thread(target=broker_utils.setup_consumer)
    consumer_thread.start()


@app.get("/download/{token}/{file_uid}/")
async def download_file(
        token: str, file_uid: str, start: int = 0, end: int = None,
        session: Session = Depends(base.get_session)
):
    file_token = crud.get_filetoken_by_token(session, token_str=token, file_uid=file_uid)
    if not file_token:
        raise HTTPException(status_code=404, detail="File not found")

    file_size = os.path.getsize(file_token.fileinfo.file_path)
    print(file_size)
    if end is None or end >= file_size:
        end = file_size - 1

    if start < 0 or end < start:
        raise HTTPException(status_code=400, detail="Invalid range")

    def iter_file():
        with open(file_token.fileinfo.file_path, mode="rb") as file:
            file.seek(start)
            remaining_bytes = end - start + 1
            while remaining_bytes > 0:
                chunk_size = min(remaining_bytes, 65536)
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                remaining_bytes -= len(chunk)
                yield chunk

    headers = {
        "Content-Type": "application/octet-stream",
        "Content-Disposition": f"attachment; filename={file_token.fileinfo.file_uid}",
        "Content-Range": f"bytes {start}-{end}/{file_size}",
    }
    return StreamingResponse(iter_file(), headers=headers)

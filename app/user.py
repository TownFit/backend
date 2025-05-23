from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.db import get_db
from app import crud


# 현재 로그인한 유저 조회
def get_current_user(request: Request, dbSession: Session = Depends(get_db)):
    if "user" not in request.session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = crud.get_user(dbSession, request.session["user"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

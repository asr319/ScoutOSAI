from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db import SessionLocal
from app.services.user_service import UserService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserIn(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserIn, db: Session = Depends(get_db)):
    service = UserService(db)
    if service.get_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username taken")
    new_user = service.create_user({"username": user.username, "password": user.password})
    return {"message": "User registered", "id": new_user.id}

@router.post("/login")
def login(user: UserIn, db: Session = Depends(get_db)):
    service = UserService(db)
    db_user = service.get_by_username(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        service.pw_hasher.verify(db_user.password_hash, user.password)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "id": db_user.id}


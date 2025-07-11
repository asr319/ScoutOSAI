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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserIn(BaseModel):
    username: str
    password: str

@router.post("/create")
def create_user(user: UserIn):
    # TODO: Create user in database
    return {"message": "User created", "user": user}

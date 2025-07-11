from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import hashlib

router = APIRouter()

fake_users = []  # Replace with real DB in production

class UserIn(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserIn):
    if any(u["username"] == user.username for u in fake_users):
        raise HTTPException(status_code=400, detail="Username taken")
    user_entry = {
        "username": user.username,
        "password_hash": hashlib.sha256(user.password.encode()).hexdigest(),
        "id": len(fake_users) + 1
    }
    fake_users.append(user_entry)
    return {"message": "User registered", "id": user_entry["id"]}

@router.post("/login")
def login(user: UserIn):
    for u in fake_users:
        if u["username"] == user.username and u["password_hash"] == hashlib.sha256(user.password.encode()).hexdigest():
            return {"message": "Login successful", "id": u["id"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

from typing import Any, Dict, Generator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import pyotp
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.auth_service import create_access_token, verify_token
from app.services.user_service import UserService
from app.services.user_profile_service import UserProfileService

router = APIRouter()
security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RegisterUserIn(BaseModel):
    username: str
    password: str
    role: str | None = "user"


class LoginUserIn(BaseModel):
    username: str
    password: str
    totp_code: str


class ProfileIn(BaseModel):
    user_id: int
    preferences: Dict[str, Any]


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    return verify_token(credentials.credentials)


@router.post("/register")
def register(user: RegisterUserIn, db: Session = Depends(get_db)) -> Dict[str, Any]:
    service = UserService(db)
    if service.get_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username taken")
    new_user = service.create_user(
        {
            "username": user.username,
            "password": user.password,
            "role": user.role,
        }
    )
    return {
        "message": "User registered",
        "id": new_user.id,
        "totp_secret": new_user.totp_secret,
    }


@router.post("/login")
def login(user: LoginUserIn, db: Session = Depends(get_db)) -> Dict[str, Any]:
    service = UserService(db)
    db_user = service.get_by_username(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        service.pw_hasher.verify(db_user.password_hash, user.password)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    totp = pyotp.TOTP(db_user.totp_secret)
    if not totp.verify(user.totp_code):
        raise HTTPException(status_code=401, detail="Invalid TOTP code")
    token = create_access_token({"sub": str(db_user.id), "role": db_user.role})
    return {"message": "Login successful", "id": db_user.id, "token": token}


@router.get("/profile")
def get_profile(
    user_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    if user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")
    service = UserProfileService(db)
    profile = service.get_profile(user_id)
    prefs = profile.preferences if profile else {}
    return {"user_id": user_id, "preferences": prefs}


@router.put("/profile")
def update_profile(
    payload: ProfileIn,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    if payload.user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized")
    service = UserProfileService(db)
    profile = service.update_profile(payload.user_id, payload.preferences)
    return {
        "message": "Profile updated",
        "profile": {"user_id": profile.user_id, "preferences": profile.preferences},
    }

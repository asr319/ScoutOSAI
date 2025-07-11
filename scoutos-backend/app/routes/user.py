from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UserIn(BaseModel):
    username: str
    email: str

@router.post("/create")
def create_user(user: UserIn):
    # TODO: Create user in database
    return {"message": "User created", "user": user}

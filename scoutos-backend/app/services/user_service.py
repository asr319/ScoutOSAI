# Placeholder for user-related business logic

from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.models.user import User


class UserService:
    """Service layer for ``User`` creation and lookup."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.pw_hasher = PasswordHasher()

    def create_user(self, user_data: dict) -> User:
        """Create a new ``User`` with a hashed password."""

        hashed = self.pw_hasher.hash(user_data["password"])
        db_user = User(username=user_data["username"], password_hash=hashed)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_username(self, username: str) -> User | None:
        """Retrieve a ``User`` by username."""

        return self.db.query(User).filter(User.username == username).first()

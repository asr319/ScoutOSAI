from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile


class UserProfileService:
    """Service for creating and updating ``UserProfile`` rows."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_profile(self, user_id: int) -> UserProfile | None:
        return self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    def update_profile(self, user_id: int, preferences: dict) -> UserProfile:
        profile = self.get_profile(user_id)
        if profile is None:
            profile = UserProfile(user_id=user_id, preferences=preferences)
            self.db.add(profile)
        else:
            profile.preferences = preferences
        self.db.commit()
        self.db.refresh(profile)
        return profile

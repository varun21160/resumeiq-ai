from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """
        Fetch a user by email.
        """
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_id(self, user_id: str) -> User | None:
        """
        Fetch a user by ID.
        """
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create_user(
        self,
        user: UserCreate,
        hashed_password: str,
    ) -> User:
        """
        Create and persist a new user.
        """
        db_user = User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hashed_password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, user: UserCreate):
        """
        Register a new user.
        """

        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered.",
            )

        hashed_password = hash_password(user.password)

        created_user = self.user_repository.create_user(
            user=user,
            hashed_password=hashed_password,
        )

        return created_user

    def login(self, email: str, password: str):
        """
        Authenticate user and return JWT.
        """

        user = self.user_repository.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

        access_token = create_access_token(subject=user.id)

        return {
            "access_token": access_token,
        "token_type": "bearer",
        }
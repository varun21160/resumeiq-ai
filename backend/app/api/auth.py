from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.register(user)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.login(
        email=form_data.username,
        password=form_data.password,
    )
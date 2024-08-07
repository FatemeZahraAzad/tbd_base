from ....api.v1.schemas.auth_schemas import UserCreate, UserRead, UserUpdate, TokenResponse
from ....api.v1.services.auth_service import AuthService
from ....api.dependencies import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/auth")


@router.post("/signup")
def register_user(user_data: UserCreate, auth_service: AuthService = Depends(AuthService)):
    user, status_code = auth_service.register_user(user_data)
    return user, status_code


@router.post("/login", response_model=TokenResponse)
def login_user(user: UserCreate, service: AuthService = Depends(AuthService)):
    """
    Login a user and get an access token.
    """
    return service.login_user(user)


@router.get("/me", response_model=UserRead)
def get_current_user(user=Depends(get_current_user)):
    """
    Get the currently authenticated user.
    """
    return user


@router.put("/me", response_model=UserRead)
def update_current_user(user_update: UserUpdate, user=Depends(get_current_user),
                        service: AuthService = Depends(AuthService)):
    """
    Update the currently authenticated user.
    """
    return service.update_user(user, user_update)

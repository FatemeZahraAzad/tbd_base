import os
from .api.v1.schemas.auth_schemas import UserCreate
from .api.v1.services.auth_service import AuthService
from .core.token_generator import TokenGenerator
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .core.database import get_db
from .core.security import verify_password, create_access_token
from .models.user import UserModel
from fastapi import FastAPI, HTTPException, status, Depends
from .api.v1.routes.auth import router as auth_router

router = APIRouter()

app = FastAPI()
app.include_router(auth_router)

# Initialize the TokenGenerator with your secret key
token_generator = TokenGenerator(secret_key=os.getenv('SECRET_KEY'))


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login endpoint.
    """
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/signup/")
def register_user(user_data: UserCreate, auth_service: AuthService = Depends(AuthService)):
    print(user_data)
    user, status_code = auth_service.register_user(user_data)
    return user, status_code


@app.get('/protected')
def protected_endpoint(access_token: str = Depends(token_generator.decode_token)):
    # This endpoint is protected and requires a valid access token
    user_id = access_token['user_id']
    return {'message': f'Welcome, user {user_id}!'}

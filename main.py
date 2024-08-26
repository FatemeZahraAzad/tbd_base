import os
from functools import wraps
import jwt
import datetime
from .models.user import TokenTable, User
from .core.token_generator import TokenGenerator
from fastapi import APIRouter
from .api.v1.routes.auth import router as auth_router
from .api.v1.schemas.auth_schemas import *
from .core.database import Base, engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .utils.helpers import create_access_token, create_refresh_token, verify_password, get_hashed_password
from .api.v1.schemas.auth_bearer import JWTBearer

router = APIRouter()

app = FastAPI()
app.include_router(auth_router)

# Initialize the TokenGenerator with your secret key
token_generator = TokenGenerator(secret_key=os.getenv('SECRET_KEY'))


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"  # should be kept secret
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"



def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()


@app.post('/login', response_model=TokenSchema)
def login(request: requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = TokenTable(user_id=user.id, access_toke=access, refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@app.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # existing_user = session.query(User).filter_by(email=user.email).first()
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    print("here*************************************************************************************")
    encrypted_password = get_hashed_password(user.password)

    new_user = User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "user created successfully"}


@app.get('/getusers')
def getusers(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    user = session.query(User).all()
    return user


@app.post('/change-password')
def change_password(request: changepassword, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}


@app.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(TokenTable).all()
    info = []
    for record in token_record:
        print("record", record)
        if (datetime.utcnow() - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        existing_token = db.query(TokenTable).where(TokenTable.user_id.in_(info)).delete()
        db.commit()

    existing_token = db.query(TokenTable).filter(TokenTable.user_id == user_id,
                                                        TokenTable.access_toke == token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message": "Logout Successfully"}


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        data = kwargs['session'].query(TokenTable).filter_by(user_id=user_id, access_toke=kwargs['dependencies'],
                                                                    status=True).first()
        if data:
            return func(kwargs['dependencies'], kwargs['session'])

        else:
            return {'msg': "Token blocked"}

    return wrapper


@app.get('/protected')
def protected_endpoint(access_token: str = Depends(token_generator.decode_token)):
    # This endpoint is protected and requires a valid access token
    user_id = access_token['user_id']
    return {'message': f'Welcome, user {user_id}!'}

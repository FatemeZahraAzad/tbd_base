from pydantic import BaseModel, EmailStr
import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from pydantic import BaseModel
from ....models.user import User

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import Column


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_sqlalchemy

    @classmethod
    def validate_to_sqlalchemy(cls, v):
        if isinstance(v, cls):
            username: "Column[str]" = User.__table__.c.username
            email: "Column[str]" = User.__table__.c.email
            hashed_password: "Column[str]" = User.__table__.c.hashed_password

            cls.__fields__["username"].type_ = Mapped[str]
            cls.__fields__["username"].alias = username
            cls.__fields__["email"].type_ = Mapped[str]
            cls.__fields__["email"].alias = email
            cls.__fields__["hashed_password"].type_ = Mapped[str]
            cls.__fields__["hashed_password"].alias = hashed_password
            return v
        raise ValueError("Invalid input type")


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class requestdetails(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class changepassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime

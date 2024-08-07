from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Mapped, mapped_column
from ....models.user import UserModel

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from pydantic import BaseModel
from ....models.user import UserModel

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import Column


class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_sqlalchemy

    @classmethod
    def validate_to_sqlalchemy(cls, v):
        if isinstance(v, cls):
            username: "Column[str]" = UserModel.__table__.c.username
            email: "Column[str]" = UserModel.__table__.c.email
            hashed_password: "Column[str]" = UserModel.__table__.c.hashed_password

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

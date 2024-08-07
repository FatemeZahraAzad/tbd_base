from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    chat_messages = relationship("ChatModel", backref="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}')"
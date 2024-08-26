from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Database connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://admin:1234!@#$asdfASDF@localhost:5432/postgres@localhost"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create the scoped session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Create the Base class for declarative models
Base = declarative_base()


# Dependency for getting a db session
def get_db():
    try:
        db = db_session()
        yield db
    finally:
        db_session.remove()


class SessionLocal:
    pass
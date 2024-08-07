import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

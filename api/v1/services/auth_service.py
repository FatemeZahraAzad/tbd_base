from fastapi import Depends, HTTPException, status
from ..schemas.auth_schemas import UserCreate
from typing import Tuple


class AuthService:
    def register_user(self, user_data: UserCreate) -> Tuple[dict, int]:
        # Here, you would implement the logic to create a new user:
        # - Check if the username or email is already taken
        # - Hash the password
        # - Create a new user record in the database

        # For this example, we'll just return the submitted data
        return user_data.dict(), status.HTTP_201_CREATED
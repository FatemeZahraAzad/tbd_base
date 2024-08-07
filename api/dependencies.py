from fastapi import Depends, HTTPException, status
from ..models.user import UserModel
from ..core.token_generator import TokenGenerator


async def get_current_user(token):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    user = UserModel.query.get(token.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

import os
import time
import jwt
from datetime import datetime, timedelta
from typing import Dict


class TokenGenerator:
    """
    Class to generate and manage access tokens.
    """

    def __init__(self, secret_key: str, algorithm: str = 'HS256', token_lifetime: int = 3600):
        """
        Initialize the TokenGenerator class.

        Args:
            secret_key (str): The secret key used to sign the JWT tokens.
            algorithm (str, optional): The algorithm used to sign the JWT tokens. Defaults to 'HS256'.
            token_lifetime (int, optional): The lifetime of the tokens in seconds. Defaults to 3600 (1 hour).
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_lifetime = token_lifetime

    def generate_access_token(self, user_id: str) -> str:
        """
        Generate an access token for the given user ID.

        Args:
            user_id (str): The user ID to generate the token for.

        Returns:
            str: The generated access token.
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.token_lifetime)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, str]:
        """
        Decode and verify the given access token.

        Args:
            token (str): The access token to decode.

        Returns:
            dict: The decoded payload of the token.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.exceptions.DecodeError:
            raise ValueError("Invalid token")

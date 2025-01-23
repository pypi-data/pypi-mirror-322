from datetime import datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


class JWTHandler:
    import os

    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not SECRET_KEY:
        raise EnvironmentError('JWT_SECRET_KEY environment variable is not set')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self, secret_key=None, algorithm=None, expire_minutes=None):
        if secret_key:
            self.SECRET_KEY = secret_key
        if algorithm:
            self.ALGORITHM = algorithm
        if expire_minutes:
            self.ACCESS_TOKEN_EXPIRE_MINUTES = expire_minutes

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(
                token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            email: str = payload.get('sub')
            if email is None:
                raise InvalidTokenError
            return email
        except (ExpiredSignatureError, InvalidTokenError):
            raise InvalidTokenError


def new(secret_key=None, algorithm=None, expire_minutes=None) -> JWTHandler:
    return JWTHandler(secret_key, algorithm, expire_minutes)

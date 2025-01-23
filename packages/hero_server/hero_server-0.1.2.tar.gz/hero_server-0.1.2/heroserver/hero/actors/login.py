from tabella import Tabella
from pydantic import BaseModel, Field, EmailStr, validator
from openrpc import BearerAuth, Depends, RPCRouter
import bcrypt
import datetime
from typing import List, Optional
from fastapi import Depends, Request
from starlette.datastructures import Headers
import time
from actors.mydb import db
from actors.circle.user import *
from jose import jwt

db_cat = "user"
router = RPCRouter()

# openssl rand -hex 32
SECRET_KEY = "f5d94a66702b1c932df8e4e4aa99402ab581d2e19883c618b67d5593af05c9c7"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str


security_scheme = {"Bearer": BearerAuth()}

def get_user(caller_details: Headers) -> User:
    """Get caller user object from request headers."""
    auth = caller_details.get("Authorization")
    if auth is None:
        raise PermissionError("No user is signed in.")
    access_token = auth.removeprefix("Bearer ")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db[payload["username"]]
    return user


@router.method(security={"Bearer": []})
def get_caller(user: User = Depends(get_user)) -> User:
    """Get the user calling this method."""
    return user


@router.method(security={"Bearer": ["scope1"]})
def require_scopes() -> bool:
    """Require caller to have security scope `scope`."""
    return True


@router.method()
async def sign_up(username: str, password: str, pubkey: str, name: str, ipaddr:str, email: EmailStr, mobile: str, signatures: List[Signature] ) -> None:
    """Create a new user."""
    byte_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt()).decode()
    user = User(username=username, hashed_password=hashed_password, pubkey=pubkey, name=name, ipaddr=ipaddr, email=email, mobile=mobile, signatures=signatures, security_schemes={"Bearer": []},)
    await set_user(user)
    db[user.username] = user

@router.method()
def sign_in(username: str, password: str) -> Token:
    """Get a JWT for an existing user."""
    user = db[username]
    # Incorrect password.
    if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise Exception("Authentication failed.")

    return Token(
        access_token=_create_access_token(
            data={"username": user.username}, lifespan=datetime.timedelta(hours=1.0)
        ),
        token_type="bearer",
    )


def _create_access_token(data: dict, lifespan: datetime.timedelta) -> str:
    """Create an access token with encoded data."""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + lifespan
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

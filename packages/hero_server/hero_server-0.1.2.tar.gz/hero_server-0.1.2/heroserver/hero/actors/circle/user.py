from tabella import Tabella
from pydantic import BaseModel, Field, EmailStr, validator
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB
from actors.mydb import db
import time
import string
import random


router = RPCRouter()
db_cat = "user"

from actors.circle.signature import Signature


class User(BaseModel):
    oid: str = Field(
        default="", description="Unique ID for user in a circle", example="a7c"
    )
    signatures: List[Signature] = Field(
        ...,
        description="Signatures associated with the user",
        examples=[
            Signature(
                pubkey="".join(
                    random.choices(string.ascii_uppercase + string.digits, k=32)
                ),
                content="content",
                signature="".join(
                    random.choices(string.ascii_uppercase + string.digits, k=32)
                ),
                time_creation=int(time.time()),
            )
        ],
    )
    comments: List[str] = Field(
        description="List of oid's of comments linked to this story",
        examples=["some comment"],
    )
    time_creation: int = Field(
        default=0,
        description="Time when signature was created, in epoch",
        examples=[1711442827],
    )
    pubkey: str = Field(
        min_length=8,
        description="Unique key for a user, is on blockchain solana, also address where money goes",
        examples=["3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX"],
    )
    name: str = Field(
        min_length=5,
        description="Chosen name by user, needs to be unique on tfgrid level",
        examples=["myname"],
    )
    ipaddr: str = Field(
        default="",
        description="Mycelium IP address",
        examples=["fe80::5f21:d7a2:5c8e:ecf0"],
    )
    email: List[EmailStr] = Field(
        description="Email addresses", examples=["info@example.com", "other@email.com"]
    )
    mobile: List[str] = Field(description="Mobile numbers", examples=["+3244444444"])


@router.method()
def set(user: User) -> int:
    user_id = db.set(
        user,
        uniq=["oid", "name", "pubkey"],
        toindex=["ipaddr", "email", "mobile", "time_creation"],
    )
    return user_id


@router.method()
def get(oid: str) -> Optional[User]:
    json_data = db.get(cat="user", oid=oid)

    if isinstance(json_data, str):
        return User.model_validate_json(json_data)
    return None


@router.method()
def delete(oid: str):
    db.delete(cat="user", oid=oid)


class UserFilter(BaseModel):
    pubkey: Optional[str] = Field(
        None,
        description="User public key",
        examples=[
            "".join(random.choices(string.ascii_uppercase + string.digits, k=32))
        ],
    )
    name: Optional[str] = Field(
        None, description="User name", examples=["my_user_name"]
    )
    ipaddr: Optional[str] = Field(
        None, description="Mycelium IP address", examples=["fe80::5f21:d7a2:5c8e:ecf0"]
    )
    email: Optional[str] = Field(
        None, description="User email", examples=["info@example.com", "other@email.com"]
    )
    mobile: Optional[str] = Field(
        None, description="Mobile number", examples=["+3244444444"]
    )
    from_time_creation: Optional[int] = Field(
        None,
        description="used to include users with this time_creation value or higher",
        examples=[1711442827],
    )
    to_time_creation: Optional[int] = Field(
        None,
        description="used to include users with this time_creation value of less",
        examples=[1711442827],
    )


@router.method()
def list(args: UserFilter) -> List[User]:
    kwargs = args.dict(exclude_none=True)
    if "email" in kwargs:
        kwargs["email"] = [item.strip() for item in kwargs["email"].split(",")]
    if "mobile" in kwargs:
        kwargs["mobile"] = [item.strip() for item in kwargs["mobile"].split(",")]
    if "from_time_creation" in kwargs:
        kwargs["time_creation__gte"] = kwargs.pop("from_time_creation")
    if "to_time_creation" in kwargs:
        kwargs["time_creation__lte"] = kwargs.pop("to_time_creation")
    users_json = db.find("user", **kwargs)
    users = [User.model_validate_json(result.data) for result in users_json]
    return users

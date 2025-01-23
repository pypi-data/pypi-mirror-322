from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from openrpc import RPCRouter
import redis




# Redis connection setup
redis_conn = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

# RPC Router for method handling
router = RPCRouter()

# Redis Hash Key Prefix
hsetkey = "hero:user"
class Signature(BaseModel):
    pubkey: str = Field(..., description="The public key of the signer", example="3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX")
    content: str = Field(..., description="Content that got signed", example="some content")
    signature: str = Field(..., description="Signature of the content", example="5eykt4dfasdfadfadfEpY1vzqKqZKvdpHGqpCD3ZKFSs")
    time_creation: int = Field(default=0,default_factory=lambda: int(datetime.now().timestamp()), description="Time when signature was created, in epoch")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    hashed_password: str
    security_schemes: dict[str, list[str]]
    pubkey: str = Field(..., description="Unique key for a user, is on blockchain solana, also address where money goes", example="3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX")
    name: str = Field(..., description="Chosen name by user, needs to be unique on tfgrid level", example="myname")
    ipaddr: str = Field(..., description="Mycelium IP address", example="fe80::5f21:d7a2:5c8e:ecf0")
    email: EmailStr = Field(..., description="Email address", example="info@example.com")
    mobile: str = Field(..., description="Mobile number", example="+324444444")
    signatures: List[Signature] = Field(..., description="Signature of pubkey+email+mobile as done by private key on solana by the user")

    # @validator('signature', pre=True, always=True)
    # def default_signature(cls, v):
    #     return v or []



async def set(user: User) -> User:
    user_json = user.model_dump_json()
    redis_conn.hset(hsetkey, user.pubkey, user_json)
    return user

@router.method()
async def get(pubkey: str) -> Optional[User]:
    user_json = redis_conn.hget(hsetkey, pubkey)
    if user_json:
        return User.model_validate_json(user_json)
    return None

@router.method()
async def delete(pubkey: str) -> bool:
    return redis_conn.hdel(hsetkey, pubkey) > 0

class UserFilter(BaseModel):
    pubkey: Optional[str] = None
    name: Optional[str] = None
    ipaddr: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None

@router.method(security={"Bearer": []})
async def list(filters: UserFilter) -> List[User]:
    users_json = redis_conn.hvals(hsetkey)
    print(users_json)
    users = [User.model_validate_json(user_json) for user_json in users_json]

    def user_matches(user: User, filters: UserFilter) -> bool:
        if filters.pubkey and filters.pubkey != user.pubkey:
            return False
        if filters.name and filters.name != user.name:
            return False
        if filters.ipaddr and filters.ipaddr != user.ipaddr:
            return False
        if filters.email and filters.email != user.email:
            return False
        if filters.mobile and filters.mobile != user.mobile:
            return False
        return True

    return [user for user in users if user_matches(user, filters)]

from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from openrpc import RPCRouter
from heroserver.openrpc.actors.user_old import Signature
import redis

# Redis connection setup
redis_conn = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

# RPC Router for method handling
router = RPCRouter()

# Redis Hash Key Prefix
hsetkey = "hero:circle"


class Circle(BaseModel):
    pubkey: str = Field(..., description="Unique public key for account which is linked to group (all admins are signer)", example="3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX")
    name: str = Field(..., description="Chosen name by user, needs to be unique on tfgrid level", example="mycircle")
    admins: List[str] = Field(..., description="List of the pubkeys of the admins, admins can change the group")
    stakeholders: List[str] = Field(..., description="List of people who are stakeholders (are also members)")
    members: List[str] = Field(..., description="List of members in the group (can contribute)")
    viewers: List[str] = Field(..., description="List of people who can only see info in group")
    admin_quorum: int = Field(..., description="Nr of signers needed for e.g. using treasury of group")
    signatures: List[Signature] = Field(..., description="Signatures which validate the circle")
    description: str = Field(..., description="Describe the circle", example="lets put some content for the circle here")

    @validator('signatures', pre=True, always=True)
    def default_signatures(cls, v):
        return v or []

@router.method()
async def set(circle: Circle) -> Circle:
    circle_json = circle.model_dump_json()
    redis_conn.hset(hsetkey, circle.pubkey, circle_json)
    return circle

@router.method()
async def get(pubkey: str) -> Optional[Circle]:
    circle_json = redis_conn.hget(hsetkey, pubkey)
    if circle_json:
        return Circle.model_validate_json(circle_json)
    return None

@router.method()
async def delete(pubkey: str) -> bool:
    return redis_conn.hdel(hsetkey, pubkey) > 0

class CircleFilter(BaseModel):
    pubkey: Optional[str] = None
    name: Optional[str] = None

@router.method()
async def list(filters: CircleFilter) -> List[Circle]:
    circles_json = redis_conn.hvals(hsetkey)
    circles = [Circle.model_validate_json(circle_json) for circle_json in circles_json]

    def circle_matches(circle: Circle, filters: CircleFilter) -> bool:
        if filters.pubkey and filters.pubkey != circle.pubkey:
            return False
        if filters.name and filters.name != circle.name:
            return False
        return True

    return [circle for circle in circles if circle_matches(circle, filters)]

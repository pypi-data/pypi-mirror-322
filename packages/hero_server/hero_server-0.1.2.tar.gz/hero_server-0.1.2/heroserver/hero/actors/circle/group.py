from pydantic import BaseModel, Field
from openrpc import RPCRouter
import redis
from typing import List, Optional

# Setup Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)

# Initialize RPC Router for method handling
router = RPCRouter()

# Redis Hash Key Prefix for groups
hsetkey = "hero:group"


class Group(BaseModel):
    circle: str = Field(
        ...,
        description="The pubkey of the circle this group belongs to",
        examples=["3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX"],
    )
    name: str = Field(
        ...,
        description="The name of the group, unique per circle",
        examples=["mygroup"],
    )
    pubkeys: List[str] = Field(
        ...,
        description="List of pubkeys of group members",
        examples=["3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX"],
    )


@router.method()
async def set(group: Group) -> Group:
    group_json = group.model_dump_json()
    redis_conn.hset(hsetkey, group.circle + ":" + group.name, group_json)
    return group


@router.method()
async def get(circle: str, name: str) -> Optional[Group]:
    group_json = redis_conn.hget(hsetkey, circle + ":" + name)
    if group_json:
        return Group.model_validate_json(group_json)
    return None


@router.method()
async def delete(circle: str, name: str) -> bool:
    return redis_conn.hdel(hsetkey, circle + ":" + name) > 0


class GroupFilter(BaseModel):
    circle: Optional[str] = Field(None, description="Filter by the circle pubkey")
    name: Optional[str] = Field(None, description="Filter by the group name")


@router.method()
async def list(filters: GroupFilter) -> List[Group]:
    groups_json = redis_conn.hvals(hsetkey)
    groups = [Group.model_validate_json(group_json) for group_json in groups_json]

    def group_matches(group: Group, filters: GroupFilter) -> bool:
        if filters.circle and filters.circle != group.circle:
            return False
        if filters.name and filters.name != group.name:
            return False
        return True

    return [group for group in groups if group_matches(group, filters)]

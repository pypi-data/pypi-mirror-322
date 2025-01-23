from pydantic import BaseModel, Field
from openrpc import RPCRouter
import redis
from typing import List, Optional,Enum
from tools.secret.box import *
import json

# Setup Redis connection
redis_conn = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

# Initialize RPC Router for method handling
router = RPCRouter()

# Redis Hash Key Prefix for groups
hsetkey = "hero:stellar"


class NetworkType(str, Enum):
    pubnet = "pubnet"
    testnet = "testnet"

class BCAccount(BaseModel):
    name: constr(min_length=4, max_length=20) = Field(..., description="Name for your account.")
    secret: constr(min_length=56, max_length=56) = Field(..., description="The secret key of the existing account to fund the new account, only needed for pubnet.")
    network: NetworkType = Field(..., description="Network type: pubnet or testnet.")

@router.method()
def account_register(account: BCAccount):
    """
    Register your account, will be encrypted using your secretbox.
    """

    # Store data in Redis with an expiration of 12 hours (43200 seconds)
    b=box_get()

    ##encrypt the secret
    account.secret=b.encrypt(account.secret.encode())

    group_json = account.model_dump_json()

    redis_conn.hset(hsetkey,account.name, group_json)

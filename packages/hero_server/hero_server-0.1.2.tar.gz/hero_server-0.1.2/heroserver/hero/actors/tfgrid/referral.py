from tabella import Tabella
from pydantic import BaseModel, Field
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB
from actors.mydb import db
import time
from enum import Enum

router = RPCRouter()
db_cat = "referral"

class RewardType(str, Enum):
    l1 = "l1"  # is first level reward
    l2 = "l2"  # is 2nd level reward

class Reward(BaseModel):
    reward_time: int = Field(..., description="Time when reward was done (as epoch)", example=1711442827)
    asset_type: str = Field(..., description="e.g. INCA, TFT", example="tft")
    amount: int = Field(..., description="Amount of tokens send", example=100)
    transaction_id: str = Field(..., description="To find back on blockchain, is a transaction id on solana")
    reward_type: RewardType = Field(..., description="Reward type")

class Referral(BaseModel):
    oid: str = Field(default="",description="Unique ID in a circle", example="a7c")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    pubkey_existing_user: str = Field(..., description="The one who received the invitations")
    pubkey_new_user: str = Field(..., description="The ones who get the invitation")
    time_invited: int = Field(..., description="Time invitation was sent", example=1711442827)
    time_installed: int = Field(..., description="Time when tfconnect was installed (epoch)", example=1711442827)
    rewards: List[Reward] = Field(..., description="List of rewards")

@router.method()
def set(referral: Referral) -> int:
    json_data = referral.model_dump_json()
    referral_id = db.set("referral", referral.oid, json_data, pubkey_existing_user=referral.pubkey_existing_user, pubkey_new_user=referral.pubkey_new_user, time_invited=referral.time_invited, time_installed=referral.time_installed)
    return referral_id

@router.method()
def get(oid: Optional[str] = None, pubkey_existing_user: Optional[str] = None, pubkey_new_user: Optional[str] = None) -> Optional[Referral]:
    if oid:
        json_data = db.get("referral", oid)
    elif pubkey_existing_user or pubkey_new_user:
        kwargs = {}
        if pubkey_existing_user:
            kwargs["pubkey_existing_user"] = pubkey_existing_user
        if pubkey_new_user:
            kwargs["pubkey_new_user"] = pubkey_new_user
        results = db.find("referral", **kwargs)
        if results:
            json_data = results[0].data
        else:
            json_data = None
    else:
        json_data = None

    if json_data:
        return Referral.model_validate_json(json_data)
    return None

@router.method()
def delete(oid: str):
    db.delete("referral", oid)

class ReferralFilter(BaseModel):
    from_time_invited: Optional[int] = None
    to_time_invited: Optional[int] = None
    from_time_installed: Optional[int] = None
    to_time_installed: Optional[int] = None
    pubkey_existing_user: Optional[str] = None
    pubkey_new_user: Optional[str] = None

@router.method()
def list(args: ReferralFilter) -> List[Referral]:
    kwargs = args.dict(exclude_none=True)
    if "from_time_invited" in kwargs:
        kwargs["time_invited__gte"] = kwargs.pop("from_time_invited")
    if "to_time_invited" in kwargs:
        kwargs["time_invited__lte"] = kwargs.pop("to_time_invited")
    if "from_time_installed" in kwargs:
        kwargs["time_installed__gte"] = kwargs.pop("from_time_installed")
    if "to_time_installed" in kwargs:
        kwargs["time_installed__lte"] = kwargs.pop("to_time_installed")
    referrals_json = db.find("referral", **kwargs)
    referrals = [Referral.model_validate_json(result.data) for result in referrals_json]
    return referrals

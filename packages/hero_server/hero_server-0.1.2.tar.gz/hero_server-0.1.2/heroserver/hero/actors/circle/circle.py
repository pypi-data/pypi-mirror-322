from tabella import Tabella
from pydantic import BaseModel, Field, validator
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB
from actors.mydb import db
import time
import string
import random

router = RPCRouter()
db_cat = "circle"

from actors.circle.signature import Signature


class Group(BaseModel):
    name: str = Field(
        ...,
        description="The name of a group, unique per circle",
        examples=["group_name"],
    )
    members: List[str] = Field(
        description="List of gids which are globally unique ids, is cid.oid",
        example=["abc.a3f6"],
    )


class Circle(BaseModel):
    oid: str = Field(
        default="", description="Unique ID for user in a circle", examples=["a7c"]
    )
    signatures: List[Signature] = Field(
        ...,
        description="Signatures associated with the circle",
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
        ...,
        description="List of oid's of comments linked to this story",
        examples=["first comment"],
    )
    time_creation: int = Field(
        default=0,
        description="Time when signature was created, in epoch",
        examples=[1711442827],
    )
    pubkey: str = Field(
        ...,
        description="Unique public key for account which is linked to group (all admins are signer)",
        examples=["AABBCCDDEEFFGG"],
    )
    name: str = Field(
        ...,
        description="Chosen name by user, needs to be unique on tfgrid level",
        examples=["myclub1"],
    )
    description: str = Field(
        ..., description="Description of the circle", examples=["my football club"]
    )
    admins: List[str] = Field(
        ...,
        description="List of the pubkeys of the admins, admins can change the group",
        examples=[
            "".join(random.choices(string.ascii_uppercase + string.digits, k=32))
        ],
    )
    stakeholders: List[str] = Field(
        ...,
        description="List of people who are stakeholders (are also members)",
        examples=["first_stakeholder"],
    )
    members: List[str] = Field(
        ...,
        description="List of members in the group (can contribute)",
        examples=["first_member"],
    )
    viewers: List[str] = Field(
        ...,
        description="List of people who can only see info in group",
        examples=["first_viewer"],
    )
    admin_quorum: int = Field(
        description="Number of signers needed for e.g. using treasury of group",
        examples=[10],
    )
    groups: List[Group] = Field(
        ...,
        description="To define one or more groups in the circle",
        examples=[Group(name="mygroup", members=["firstmember", "secondmember"])],
    )


@router.method()
def set(circle: Circle) -> int:
    if circle.name != "":
        o = db.find("circle", name=circle.name)
        # if len(o)>0:
        #     import pdb; pdb.set_trace()

    circle = db.obj_check(circle)
    json_data = circle.model_dump_json()
    circle_id = db.set(circle, uniq=["oid", "name"], toindex=["name", "time_creation"])
    return circle_id


# this is comment for a get statement
@router.method()
def get(oid: str) -> Optional[Circle]:
    json_data = db.get(cat="circle", oid=oid)
    if json_data:
        return Circle.model_validate_json(json_data)
    return None


@router.method()
def delete(oid: str):
    db.delete(cat="circle", oid=oid)


class CircleFilter(BaseModel):
    name: Optional[str] = None
    from_time_creation: Optional[int] = None
    to_time_creation: Optional[int] = None


@router.method()
def list(args: CircleFilter) -> List[Circle]:
    kwargs = args.dict(exclude_none=True)
    if "from_time_creation" in kwargs:
        kwargs["time_creation__gte"] = kwargs.pop("from_time_creation")
    if "to_time_creation" in kwargs:
        kwargs["time_creation__lte"] = kwargs.pop("to_time_creation")
    circles_json = db.find("circle", **kwargs)
    circles = [Circle.model_validate_json(result.data) for result in circles_json]
    return circles

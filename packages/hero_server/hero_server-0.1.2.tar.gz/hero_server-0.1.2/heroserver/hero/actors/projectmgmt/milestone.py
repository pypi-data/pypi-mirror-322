from tabella import Tabella
from pydantic import BaseModel, Field
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB
from actors.mydb import db
import time

router = RPCRouter()
db_cat = "milestone"

from actors.circle.signature import Signature
from actors.projectmgmt.project import Project

class Milestone(BaseModel):
    oid: str = Field(default="",description="Unique ID for user in a circle", example="a7c")
    signatures: List[Signature] = Field(..., description="Signatures associated with the milestone")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    time_creation: int = Field(default=0, description="Time when signature was created, in epoch", example=1711442827)
    title: str = Field(..., description="Title of a milestone", example="this is our release tfgrif 3.1")
    content: str = Field(..., description="Description of the milestone", example="this is example content which gives more color")
    owners: List[str] = Field(..., description="List of people (oid) who are the owners of this project", example=["f23"])
    notifications: List[str] = Field(..., description="List of people (oid) who want to be informed of changes of this milestone", example=["ad3"])
    deadline: int = Field(..., description="Epoch deadline for the milestone", example=1711442827)
    projects: List[Project] = Field(..., description="List of projects linked to milestone")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")


@router.method()
def set(milestone: Milestone) -> int:
    json_data = milestone.model_dump_json()
    milestone_id = db.set("milestone", milestone.oid, json_data, title=milestone.title, owners=milestone.owners, notifications=milestone.notifications, deadline=milestone.deadline, time_creation=milestone.time_creation)
    return milestone_id

@router.method()
def get(oid: str) -> Optional[Milestone]:
    json_data = db.get("milestone", oid)
    if json_data:
        return Milestone.model_validate_json(json_data)
    return None

@router.method()
def delete(oid: str):
    db.delete("milestone", oid)

class MilestoneFilter(BaseModel):
    title: Optional[str] = None
    owners: Optional[str] = None
    notifications: Optional[str] = None
    from_deadline: Optional[int] = None
    to_deadline: Optional[int] = None
    from_time_creation: Optional[int] = None
    to_time_creation: Optional[int] = None

@router.method()
def list(args: MilestoneFilter) -> List[Milestone]:
    kwargs = args.dict(exclude_none=True)
    if "owners" in kwargs:
        kwargs["owners"] = [item.strip() for item in kwargs["owners"].split(',')]
    if "notifications" in kwargs:
        kwargs["notifications"] = [item.strip() for item in kwargs["notifications"].split(',')]
    if "from_deadline" in kwargs:
        kwargs["deadline__gte"] = kwargs.pop("from_deadline")
    if "to_deadline" in kwargs:
        kwargs["deadline__lte"] = kwargs.pop("to_deadline")
    if "from_time_creation" in kwargs:
        kwargs["time_creation__gte"] = kwargs.pop("from_time_creation")
    if "to_time_creation" in kwargs:
        kwargs["time_creation__lte"] = kwargs.pop("to_time_creation")
    milestones_json = db.find("milestone", **kwargs)
    milestones = [Milestone.model_validate_json(result.data) for result in milestones_json]
    return milestones

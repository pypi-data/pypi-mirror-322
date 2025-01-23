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
db_cat = "swimlane_template"

from actors.circle.signature import Signature

class SwimLane(BaseModel):
    name: str = Field(..., description="Short name for swimlane")
    purpose: str = Field(..., description="Description, purpose of swimlane")
    deadline: int = Field(..., description="Epoch deadline for the swimlane, normally not used", example=1711442827)

class SwimLaneTemplate(BaseModel):
    oid: str = Field(default="",description="Unique ID for user in a circle", example="a7c")
    signatures: List[Signature] = Field(..., description="Signatures associated with the swimlane template")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    time_creation: int = Field(default=0, description="Time when signature was created, in epoch", example=1711442827)
    name: str = Field(..., description="Name as need to be used in relation to project")
    template: List[SwimLane] = Field(..., description="Template of swimlanes")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")

class ProjectType(str, Enum):
    product = "product"
    operations = "operations"
    customerdelivery = "customerdelivery"
    other = "other"

@router.method()
def set(swimlane_template: SwimLaneTemplate) -> int:
    json_data = swimlane_template.model_dump_json()
    swimlane_template_id = db.set("swimlane_template", swimlane_template.oid, json_data, name=swimlane_template.name, time_creation=swimlane_template.time_creation)
    return swimlane_template_id

@router.method()
def get(oid: str) -> Optional[SwimLaneTemplate]:
    json_data = db.get("swimlane_template", oid)
    if json_data:
        return SwimLaneTemplate.model_validate_json(json_data)
    return None

@router.method()
def delete(oid: str):
    db.delete("swimlane_template", oid)

class SwimLaneTemplateFilter(BaseModel):
    name: Optional[str] = None
    from_time_creation: Optional[int] = None
    to_time_creation: Optional[int] = None

@router.method()
def list(args: SwimLaneTemplateFilter) -> List[SwimLaneTemplate]:
    kwargs = args.dict(exclude_none=True)
    if "from_time_creation" in kwargs:
        kwargs["time_creation__gte"] = kwargs.pop("from_time_creation")
    if "to_time_creation" in kwargs:
        kwargs["time_creation__lte"] = kwargs.pop("to_time_creation")
    swimlane_templates_json = db.find("swimlane_template", **kwargs)
    swimlane_templates = [SwimLaneTemplate.model_validate_json(result.data) for result in swimlane_templates_json]
    return swimlane_templates

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
db_cat = "project"

from actors.circle.signature import Signature
from actors.circle.requirement import Requirement
from actors.circle.story import Story
from actors.circle.swimlane_template import SwimLaneTemplate

class ProjectType(str, Enum):
    product = "product"
    operations = "operations"
    customerdelivery = "customerdelivery"
    other = "other"

class Project(BaseModel):
    oid: str = Field(default="",description="Unique ID for user in a circle", example="a7c")
    signatures: List[Signature] = Field(..., description="Signatures associated with the project")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    time_creation: int = Field(default=0, description="Time when signature was created, in epoch", example=1711442827)
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    title: str = Field(..., description="Title of a story", example="improve the UI for tfgrid 3.13")
    project_type: ProjectType = Field(..., description="Type of project")
    content: str = Field(..., description="Description of what needs to be done", example="this is example content")
    owners: List[str] = Field(..., description="List of people (oid) who are the owners of this project", example=["f23"])
    notifications: List[str] = Field(..., description="List of people (oid) who want to be informed of changes of this project", example=["ad3"])
    deadline: int = Field(..., description="Epoch deadline for the project", example=1711442827)
    requirements: List[Requirement] = Field(..., description="List of requirements to fulfill linked to project")
    stories: List[Story] = Field(..., description="List of stories linked to project")
    swimlanes: SwimLaneTemplate = Field(..., description="Used to show e.g. Kanban")

@router.method()
def set(project: Project) -> int:
    json_data = project.model_dump_json()
    project_id = db.set("project", project.oid, json_data, title=project.title, project_type=project.project_type, owners=project.owners, notifications=project.notifications, deadline=project.deadline, time_creation=project.time_creation)
    return project_id

@router.method()
def get(oid: str) -> Optional[Project]:
    json_data = db.get("project", oid)
    if json_data:
        return Project.model_validate_json(json_data)
    return None

@router.method()
def delete(oid: str):
    db.delete("project", oid)

class ProjectFilter(BaseModel):
    title: Optional[str] = None
    project_type: Optional[ProjectType] = None
    owners: Optional[str] = None
    notifications: Optional[str] = None
    from_deadline: Optional[int] = None
    to_deadline: Optional[int] = None
    from_time_creation: Optional[int] = None
    to_time_creation: Optional[int] = None

@router.method()
def list(args: ProjectFilter) -> List[Project]:
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
    projects_json = db.find("project", **kwargs)
    projects = [Project.model_validate_json(result.data) for result in projects_json]
    return projects

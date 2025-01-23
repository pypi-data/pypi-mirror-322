from tabella import Tabella
from pydantic import BaseModel, Field
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB
from actors.mydb import db
import time

router = RPCRouter()
db_cat = "story"

from actors.circle.signature import Signature
from actors.projectmgmt.requirement import Requirement
from actors.projectmgmt.issue import Issue

class Story(BaseModel):
    oid: str = Field(default="",description="Unique ID for user in a circle", example="a7c")
    signatures: List[Signature] = Field(..., description="Signatures associated with the story")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    time_creation: int = Field(default=0, description="Time when signature was created, in epoch", example=1711442827)
    title: str = Field(..., description="Title of a story", example="improve the UI for tfgrif 3.13")
    content: str = Field(..., description="Description of what needs to be done", example="this is example content")
    assignees: List[str] = Field(..., description="List of people (oid) who are the owners/executes of this story", example=["f23"])
    project: Optional[str] = Field(None, description="Optional oid for the project linked to this Story")
    swimlane: str = Field(..., description="Name of the swimlane story is on")
    milestone: List[str] = Field(..., description="Optional list of milestones linked to this Story (as oid)", example=["h62", "t3fd"])
    notifications: List[str] = Field(..., description="List of people (oid) who want to be informed of changes", example=["ad3"])
    deadline: int = Field(..., description="Epoch deadline for the Story", example=1711442827)
    requirements: List[Requirement] = Field(..., description="List of requirements to fulfill")
    issues: List[Issue] = Field(..., description="List of issues linked to story (can be bug, feature request, question, ...)")

class RequirementType(str, Enum):
    feature = "feature"
    performance = "performance"
    scale = "scale"
    operations = "operations"
    ui = "ui"
    other = "other"

class Requirement(BaseModel):
    time_creation: int = Field(default=0, description="Time when signature was created, in epoch", example=1711442827)
    requirement_type: RequirementType = Field(..., description="Requirement type")
    title: str = Field(..., description="Title of a story", example="improve the UI for tfgrif 3.13")
    content: str = Field(..., description="Description of what needs to be done", example="this is example content")
    story: Optional[str] = Field(None, description="The stories linked to requirements (as oid)", example=["h62", "t3fd"])
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")


@router.method()
def set(story: Story) -> int:
    json_data = story.model_dump_json()
    story_id = db.set("story", story.oid, json_data, title=story.title, assignees=story.assignees, project=story.project, swimlane=story.swimlane, milestone=story.milestone, notifications=story.notifications, deadline=story.deadline, time_creation=story.time_creation)
    return story_id

@router.method()
def get(oid: str) -> Optional[Story]:
    json_data = db.get("story", oid)
    if json_data:
        return Story.model_validate_json(json_data)
    return None

@router.method()
def delete(oid: str):
    db.delete("story", oid)

class StoryFilter(BaseModel):
    title: Optional[str] = None
    assignees: Optional[str] = None
    project: Optional[str] = None
    swimlane: Optional[str] = None
    milestone: Optional[str] = None
    notifications: Optional[str] = None
    from_deadline: Optional[int] = None
    to_deadline: Optional[int] = None
    from_time_creation: Optional[int] = None
    to_time_creation: Optional[int] = None

@router.method()
def list(args: StoryFilter) -> List[Story]:
    kwargs = args.dict(exclude_none=True)
    if "assignees" in kwargs:
        kwargs["assignees"] = [item.strip() for item in kwargs["assignees"].split(',')]
    if "milestone" in kwargs:
        kwargs["milestone"] = [item.strip() for item in kwargs["milestone"].split(',')]
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
    stories_json = db.find("story", **kwargs)
    stories = [Story.model_validate_json(result.data) for result in stories_json]
    return stories

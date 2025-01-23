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
db_cat = "issue"

from actors.circle.signature import Signature

class IssueType(str, Enum):
    bug = "bug"
    feature = "feature"
    question = "question"
    other = "other"
    task = "task"

class Issue(BaseModel):
    oid: str = Field(default="",description="Unique ID for user in a circle", example="a7c")
    signatures: List[Signature] = Field(..., description="Signatures associated with the issue")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    time_creation: int = Field(default=0, description="Time when signature was created, in epoch", example=1711442827)
    issue_type: IssueType = Field(..., description="Issue type")
    title: str = Field(..., description="Title of a story", example="improve the UI for tfgrif 3.13")
    content: str = Field(..., description="Description of what needs to be done", example="this is example content")
    assignees: List[str] = Field(..., description="List of people (oid) who are the owners/executes of this story", example=["f23"])
    notifications: List[str] = Field(..., description="List of people (oid) who want to be informed of changes", example=["ad3"])
    deadline: int = Field(..., description="Epoch deadline for the Story", example=1711442827)
    issues: List['Issue'] = Field(..., description="List of issues linked to story (can be bug, feature request, question, ...)")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")



@router.method()
def set(issue: Issue) -> int:
    json_data = issue.model_dump_json()
    issue_id = db.set("issue", issue.oid, json_data, issue_type=issue.issue_type, title=issue.title, assignees=issue.assignees, notifications=issue.notifications, deadline=issue.deadline, time_creation=issue.time_creation)
    return issue_id

@router.method()
def get(oid: str) -> Optional[Issue]:
    json_data = db.get("issue", oid)
    if json_data:
        return Issue.model_validate_json(json_data)
    return None

@router.method()
def delete(oid: str):
    db.delete("issue", oid)

class IssueFilter(BaseModel):
    issue_type: Optional[IssueType] = None
    title: Optional[str] = None
    assignees: Optional[str] = None
    notifications: Optional[str] = None
    from_deadline: Optional[int] = None
    to_deadline: Optional[int] = None
    from_time_creation: Optional[int] = None
    to_time_creation: Optional[int] = None

@router.method()
def list(args: IssueFilter) -> List[Issue]:
    kwargs = args.dict(exclude_none=True)
    if "assignees" in kwargs:
        kwargs["assignees"] = [item.strip() for item in kwargs["assignees"].split(',')]
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
    issues_json = db.find("issue", **kwargs)
    issues = [Issue.model_validate_json(result.data) for result in issues_json]
    return issues

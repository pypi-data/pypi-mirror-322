following are instructions of how to create a FastAPI server using OpenRPC and Tabella, and ensure that the database instance is created only once and shared with every RPC method, you can follow these steps:

we are using multiple routers in fastapi and then combine those routers in main server file called server.py

RPC Router for method handling is in each file per object
the rpcrouter is used in each file we have per object and then aggregated in the main server.py file

```python
router = RPCRouter()
```

in main file = server.py we use as example to follow (improve if needed)

```python
from fastapi import FastAPI, Request
from tabella import Tabella, Server
from osis.db import DB
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from hero.osis.actors.user import router as user_router

app = FastAPI()
tabella = Tabella(
    servers=[
        Server(name="HTTP API", url="http://localhost:8000/api"),
        Server(name="WebSocket API", url="ws://localhost:8000/api"),
    ],
)

app.starlette.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your web application's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the database instance
from actors.mydb import db

tabella.include_router(user_router, prefix="user.", tags=["User"], dependencies=[get_db])

if __name__ == "__main__":
    tabella.run()

```

we create an actor which exposes server functions as follows

```python
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
```

above is how we do crud and list on an object

the above was generated for following input

```v

pub struct Milestone {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	title string //title of a milestone example='this is our release tfgrif 3.1' *
	content string //description of the milestone="this is example content which gives more color" *
	owners []string //list of people (oid) who are the owners of this project example="f23" *
	notifications []string //list of people (oid) who want to be informed of changes of this milestone example="ad3"
	deadline int //epoch deadline for the milestone example="1711442827" *
	projects []Project //list of projects linked to milestone *
	comments []string //list of oid's of comments linked to this story
}


```

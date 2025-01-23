from tabella import Tabella
from pydantic import BaseModel, Field, validator
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB
from actors.mydb import db
import time
from enum import Enum


router = RPCRouter()
db_cat = "message"

from actors.circle.signature import Signature

class MSGType(str, Enum):
    chat = "chat"
    mail = "mail"

class ContentType(str, Enum):
    markdown = "markdown"
    text = "text"
    html = "html"
    heroscript = "heroscript"

class Message(BaseModel):
    oid: str = Field(default="",description="Unique ID for user in a circle", example="a7c")
    signatures: List[Signature] = Field(..., description="Signatures associated with the message")
    comments: List[str] = Field(..., description="List of oid's of comments linked to this story")
    time_creation: int = Field(default=0, description="Time when signature was created, in epoch", example=1711442827)
    subject: str = Field(..., description="Optional (never used for chat)")
    content: str = Field(..., description="The content of the message")
    parent: str = Field(..., description="If it's a child of other message")
    to: List[str] = Field(..., description="Unique for user")
    to_group: List[str] = Field(..., description="Unique for a group of people, see Group")
    time: int = Field(..., description="Time when message was sent (epoch)", example=1711442827)
    msg_type: MSGType = Field(..., description="e.g. chat, mail, ...")
    content_type: ContentType = Field(..., description="Content type")
    tags: str = Field(..., description="Our tag format e.g. color:red priority:urgent or just labels e.g. red, urgent (without :)")

def index_create(db: DB):
    db.index_create("message", oid=str, subject=str, parent=str, to=str, to_group=str, time_creation=int, time=int, msg_type=str, content_type=str, tags=str)

@router.method()
def set(message: Message) -> int:
    json_data = message.model_dump_json()
    message_id = db.set("message", message.oid, json_data, subject=message.subject, parent=message.parent, to=message.to, to_group=message.to_group, time_creation=message.time_creation, time=message.time, msg_type=message.msg_type, content_type=message.content_type, tags=message.tags)
    return message_id

@router.method()
def get(oid: str) -> Optional[Message]:
    json_data = db.get("message", oid)
    if json_data:
        return Message.model_validate_json(json_data)
    return None

@router.method()
def delete(oid: str):
    db.delete("message", oid)

class MessageFilter(BaseModel):
    subject: Optional[str] = None
    parent: Optional[str] = None
    to: Optional[str] = None
    to_group: Optional[str] = None
    from_time_creation: Optional[int] = None
    to_time_creation: Optional[int] = None
    from_time: Optional[int] = None
    to_time: Optional[int] = None
    msg_type: Optional[MSGType] = None
    content_type: Optional[ContentType] = None
    tags: Optional[str] = None

@router.method()
def list(args: MessageFilter) -> List[Message]:
    kwargs = args.dict(exclude_none=True)
    if "from_time_creation" in kwargs:
        kwargs["time_creation__gte"] = kwargs.pop("from_time_creation")
    if "to_time_creation" in kwargs:
        kwargs["time_creation__lte"] = kwargs.pop("to_time_creation")
    if "from_time" in kwargs:
        kwargs["time__gte"] = kwargs.pop("from_time")
    if "to_time" in kwargs:
        kwargs["time__lte"] = kwargs.pop("to_time")
    messages_json = db.find("message", **kwargs)
    messages = [Message.model_validate_json(result.data) for result in messages_json]
    return messages

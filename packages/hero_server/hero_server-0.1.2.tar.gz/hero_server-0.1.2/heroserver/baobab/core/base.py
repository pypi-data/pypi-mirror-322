from typing import List
from pydantic import BaseModel, Field


class Comment(BaseModel):
    id: int = Field(...)
    content: str = Field(...)
    author: List[int] = Field(..., description="link to users who authored the comment")


class Base(BaseModel):
    id: int = Field(...)
    circle_id: int = Field(..., description="where does this project live")
    name: str = Field(..., description="chosen name for the contract")
    description: str = Field(..., description="chosen description")
    comments: List[Comment] = Field(...)
    author: List[int] = Field(..., description="link to users who authored the object")
    created_at: int = Field(..., description="timestamp when the milestone was created")
    updated_at: int = Field(
        ..., description="timestamp when the milestone was last updated"
    )


class Base0(BaseModel):
    id: int = Field(...)
    comments: List[Comment] = Field(...)
    author: List[int] = Field(..., description="link to users who authored the object")
    moddate: int = Field(..., description="epock to mod date")


class BaseWithTag(Base):
    tag: str = Field(...)


class HeroLink(BaseModel):
    id: int = Field(...)
    ipaddr: str = Field(..., description="link to how to reach a hero")
    comments: List[Comment] = Field(..., description="all optional")
    moddate: int = Field(..., description="epoch to mod date")


class WebLink(Base):
    link: str = Field(...)


class Document(Base):
    """
    has link to the document in a circle
    """

    links: List[str] = Field(...)

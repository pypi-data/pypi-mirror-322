from typing import List
from pydantic import Field, BaseModel
from baobab.core.base import Base0


class CircleGroupSelection(BaseModel):
    circle: int = Field(..., description="link to known circle")
    group: int = Field(..., description="known group in circle")


class CircleMemberCatSelection(BaseModel):
    circle: int = Field(..., description="link to known circle")
    membership_cat: str = Field(
        ...,
        description="specify type of member, useful to select contributor, stakeholder, member or owner (comma separated)",
    )


class CircleMemberSelection(Base0):
    member_selection: List[CircleMemberCatSelection] = Field(
        ...,
        description="find other circle and members based on their membership category",
    )
    group_selection: List[CircleGroupSelection] = Field(
        ..., description="find groups of circles"
    )
    members: List[int] = Field(
        ...,
        description="manual selection of members (not resolved using groups or circles)",
    )

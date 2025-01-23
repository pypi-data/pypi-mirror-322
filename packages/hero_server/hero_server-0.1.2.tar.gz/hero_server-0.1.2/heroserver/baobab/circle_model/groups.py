from typing import List
from pydantic import Field
from baobab.core.base import Base
from .member_selection import CircleMemberSelection


class Group(Base):
    circle: int = Field(
        ..., description="link to the circle where the group belongs to"
    )
    selections: List[CircleMemberSelection] = Field(...)

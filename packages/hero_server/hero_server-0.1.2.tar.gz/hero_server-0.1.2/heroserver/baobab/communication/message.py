from baobab.core.base import BaseWithTag
from typing import List
from pydantic import Field

class Message(BaseWithTag):
    dest: List[int] = Field(..., description="manual selection where message goes too")
    cat: str = Field(..., description="enum: fireforget, chat, machine, ...")
    dest_selection: List[int] = Field(
        ...,
        description="link to CircleMemberSelection, select where message needs to go, done on circles, is optional",
    )
    documets: List[int] = Field(
        ..., description="link to documents which are relevant to message"
    )

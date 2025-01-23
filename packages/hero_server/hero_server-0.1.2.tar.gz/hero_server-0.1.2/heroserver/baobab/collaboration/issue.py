from pydantic import Field
from typing import List
from baobab.core.base import BaseWithTag


class IssueBase(BaseWithTag):
    title: str = Field(..., description="Title of the issue/story")
    sprint_id: int = Field(...)
    milestone_id: int = Field(...)
    assigned_to: List[int] = Field(..., description="Team members assigned")
    estimated_hours: float = Field(..., description="estimated hours to complete")
    actual_hours: float = Field(..., description="actual hours spent")
    perc_done: int = Field(..., description="0..100 how much is story done")
    deadline: int = Field(...)
    priority: str = Field(..., description="enum: low, normal, high, ciritcal")
    kanban_id: int = Field(..., description="kanban its linked to")
    status: str = Field(
        ...,
        description="needs to be status as corresponding to the kanban otherwise default: enum: backlog,accepted,progress,completed,verified,blocked",
    )


class Issue(IssueBase):
    story_id: int = Field(...)

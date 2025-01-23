from typing import List
from pydantic import Field, BaseModel
from baobab.core.base import BaseWithTag


class KanbanSwimlane(BaseModel):
    name: str = Field(...)
    status: str = Field(
        ..., description="enum: backlog,accepted,progress,completed,verified,blocked"
    )
    deadline: int = Field(..., description="End date for the milestone if relevant")


class Kanban(BaseWithTag):
    deadline: int = Field(..., description="deadline for this kanban")
    swimlanes: List[KanbanSwimlane] = Field(...)


class KanbanTemplate(BaseWithTag):
    deadline: int = Field(..., description="deadline for this kanban")
    swimlanes: List[KanbanSwimlane] = Field(...)

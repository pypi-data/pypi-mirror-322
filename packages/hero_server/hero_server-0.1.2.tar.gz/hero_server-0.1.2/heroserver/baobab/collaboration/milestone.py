from baobab.core.base import BaseWithTag
from pydantic import Field


class Milestone(BaseWithTag):
    deadline: int = Field(..., description="end date of the milestone")
    status: str = Field(
        ...,
        description="enum: status of the milestone : backlog,accepted,progress,completed.verified,blocked",
    )

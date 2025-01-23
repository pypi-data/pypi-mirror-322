from pydantic import Field
from baobab.core.base import BaseWithTag


class Sprint(BaseWithTag):
    goal: str = Field(..., description="goal of the sprint")
    start_date: int = Field(..., description="start date of the sprint")
    end_date: int = Field(..., description="end date of the sprint")
    status: str = Field(
        ..., description="enum: backlog,accepted,progress,completed,verified,blocked"
    )

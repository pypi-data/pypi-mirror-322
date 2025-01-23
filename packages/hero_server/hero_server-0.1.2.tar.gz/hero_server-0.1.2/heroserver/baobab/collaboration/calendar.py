from typing import List
from pydantic import Field
from baobab.core.base import BaseWithTag


class Calender(BaseWithTag):
    pass


class CalendarEvent(BaseWithTag):
    invitation: int = Field(
        ...,
        description="see circle: Invitation, shows who is part of the calendar item",
    )
    start: int = Field(..., description="epoch")
    end: int = Field(..., description="epock for end of meeting")
    calendar_name: str = Field(..., description="needs to exist as calendar")
    status: str = Field(..., description="error, scheduled, history, done")
    story_id: List[int] = Field(..., description="optional link to story")
    issue_id: List[int] = Field(..., description="optional link to issue")
    kanban_id: List[int] = Field(..., description="optional link to kanban")
    milestone_id: List[int] = Field(..., description="optional link to milestone")

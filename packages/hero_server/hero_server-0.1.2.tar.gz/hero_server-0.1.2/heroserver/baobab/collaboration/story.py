from .issue import IssueBase
from pydantic import Field
from typing import List


class Story(IssueBase):
    owners: List[int] = Field(..., description="who owns the issue/story")

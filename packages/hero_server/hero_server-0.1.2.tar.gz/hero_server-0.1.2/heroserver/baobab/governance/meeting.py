from typing import List
from pydantic import Field
from baobab.core.base import Base


class Meeting(Base):
    """
    represents a meeting e.g. a boardmeeting
    """

    purpose: str = Field(...)
    cat: str = Field(..., description="enum: boarmeeting, any, ...")
    invitation: int = Field(..., description="see collaboration: Invitation")
    votingrequests: List[int] = Field(..., description="link to VotingRequest")
    documents: List[int] = Field(
        ..., description="link to documents which can be relevant for this meeting"
    )

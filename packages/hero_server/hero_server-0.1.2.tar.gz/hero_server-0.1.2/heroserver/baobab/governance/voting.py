from pydantic import Field
from typing import List
from baobab.core.base import Base, WebLink


class VotingRequest(Base):
    """if something needs to be voted"""

    purpose: str = Field(...)
    invitation: List[int] = Field(
        ..., description="list of invitation ids (see circles)"
    )
    quorum_required: int = Field(..., description="percent of signers needed (1..100)")
    status: str = Field(..., description="enum: new, error, failed, passed")
    weblinks: List[WebLink] = Field(...)
    voting_result: int = Field(..., description="link to voting result")
    voting_start_date: int = Field(...)
    voting_expiry_date: int = Field(...)


class VotingResult(Base):
    voters: List[int] = Field(..., description="is all voters who voted pro or con")
    signatures: List[int] = Field(
        ...,
        description="link to signatures on circles, signature is on heroscript representation of voting request",
    )
    signatures_end_date: int = Field(...)
    quorum_achieved: int = Field(..., description="0..100")

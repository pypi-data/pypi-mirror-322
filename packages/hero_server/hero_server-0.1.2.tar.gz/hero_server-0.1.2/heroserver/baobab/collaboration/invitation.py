from typing import List
from baobab.core.base import BaseWithTag
from pydantic import Field, BaseModel


class InvitationRequest(BaseModel):
    invitation_message: str = Field(
        ..., description="if different compared to invitation"
    )
    request: bool = Field(
        ...,
        description="if invitation will be done to the relevant circle and members (or members of group)",
    )
    invitation_selection: List[int] = Field(
        ..., description="see circle.CircleMemberSelection"
    )
    invitees: List[int] = Field(
        ..., description="manual selection of who do you want to invite (user ids)"
    )


class InvitationAcceptance(BaseModel):
    user: int = Field(..., description="user id")
    status: str = Field(..., description="enum: no, yes, error, maybe")


class Invitation(BaseWithTag):
    purpose: str = Field(...)
    inviation_message: str = Field(
        ..., description="if specific message needs to be sent"
    )
    invitation_request: List[InvitationRequest] = Field(...)
    invitation_acceptance: List[InvitationAcceptance] = Field(...)
    deadline: int = Field(..., description="epoch")

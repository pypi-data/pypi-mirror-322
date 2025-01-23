from typing import List
from pydantic import Field
from baobab.core.base import Base
from baobab.circle_model.signature import Signature


class Circle(Base):
    pubkey: str = Field(
        ...,
        description="unique public key for account which is linked to this circle, all admins and signers",
    )
    admins: List[int] = Field(
        ..., description="List of the admins, admins can change the group"
    )
    stakeholders: List[int] = Field(
        ..., description="List of people who are stakeholders (are also members)"
    )
    members: List[int] = Field(
        ..., description="List of members in the group (can contribute)"
    )
    viewers: List[int] = Field(
        ..., description="List of people who can only see info in group"
    )
    admin_quorum: int = Field(
        ...,
        description="Nr of signers needed for e.g. using treasury of group (part of admins)",
    )
    signatures: List[Signature] = Field(
        ..., description="Signatures which validate the circle"
    )

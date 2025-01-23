from pydantic import Field
from baobab.core.base import Base0


class Signature(Base0):
    signerid: int = Field(
        ..., description="link to the signer (user), links to their pubkey"
    )
    content: str = Field(..., description="content that got signed")
    signature: str = Field(..., description="signature of the content")
    time_creation: int = Field(
        ..., description="time when signature was created, in epoch"
    )

from pydantic import Field
from typing import List
from baobab.core.base import Base, HeroLink
from .signature import Signature

# //a participant in the broadest sense possible of our ecosystem
# pub struct User {
#     core.Base
# pub mut:
#     pubkey    string    // Unique key for a user
#     ipaddr    string    // Mycelium IP address
#     signature []Signature // signature of pubkey+email+mobile as done by private key on solana by the user
#     herolinks []core.HeroLink //link how the hero of the user can be reached
#     contacts []u32 //way how we can reach a user (entity), use u32 as id
# }


class User(Base):
    """
    a participant in the broadest sense possible of our ecosystem
    """

    pubkey: str = Field(..., description="unique key for a user")
    ipaddr: str = Field(..., description="Mycelium IP address")
    signature: List[Signature] = Field(
        ...,
        description="signature of pubkey+email+mobile as done by private key on solana by the user",
    )
    herolinks: List[HeroLink] = Field(
        ..., description="link how the hero of the user can be reached"
    )
    contacts: List[int] = Field(
        ..., description="way how we can reach a user (entity), use u32 as id"
    )

from pydantic import Field
from typing import List
from baobab.core.base import Base


class Party(Base):
    """
    Struct representing a party involved in the contract
    """

    user: int = Field(..., description="link to user which is party to this contract")
    signature: int = Field(..., description="see signature in circle")


class Contract(Base):
    """
    a contract representation between people
    """

    parties: List[Party] = Field(
        ..., description="link to is underwriting the contract"
    )
    effective_date: int = Field(..., description="epoch")
    expiration_date: int = Field(..., description="epoch")
    documents: List[int] = Field(..., description="link to document ids")

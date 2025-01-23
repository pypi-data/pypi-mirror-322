from typing import List
from pydantic import Field
from .currency import CurrencyAmount
from baobab.core.base import Base, WebLink


class TransactionRequest(Base):
    """if something needs to be voted"""

    transaction_id: str = Field(
        ...,
        description="if prepared transaction on the blockchain, is the if from the blockchain (optional)",
    )
    amount: CurrencyAmount = Field(...)
    purpose: str = Field(...)
    invitation: List[int] = Field(
        ..., description="list of invitation ids (see circles)"
    )
    quorum_required: int = Field(..., description="percent of signers needed (1..100)")
    status: str = Field(..., description="enum: new, error, failed, passed")
    weblinks: List[WebLink] = Field(...)
    request_result: int = Field(..., description="link to request result")
    request_start_date: int = Field(..., description="epoch")
    request_expiry_date: int = Field(...)


class RequestResult(Base):
    voters: List[int] = Field(
        ..., description="is all voters who voted pro or con (are users)"
    )
    signatures: List[int] = Field(
        ...,
        description="link to signatures on circles, signature is on heroscript representation of request request",
    )
    signature_end_date: int = Field(...)
    quorum_achieved: int = Field(..., description="0..100")

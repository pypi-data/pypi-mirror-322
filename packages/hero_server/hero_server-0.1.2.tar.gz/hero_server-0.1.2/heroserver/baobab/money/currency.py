from pydantic import Field, BaseModel
from typing import List
from baobab.core.base import Base0, WebLink


class CurrencyAmount(BaseModel):
    amount: float = Field(..., description="amount of money in specific currency")
    currency: int = Field(..., description="link to currency")
    created_at: int = Field(..., description="timestamp when the milestone was created")
    updated_at: int = Field(
        ..., description="timestamp when the milestone was last updated"
    )


class Currency(Base0):
    asset_id: str = Field(
        ..., description="contract id if on blockchain, otherwise e.g. USD"
    )
    blockchain_type: str = Field(
        ..., description="enum: none, stellar, eth, solana, tfchain"
    )
    exchange_rate: float = Field(
        ..., description="exchange rate compared to 1 milligram of gold"
    )
    weblinks: List[WebLink] = Field(...)

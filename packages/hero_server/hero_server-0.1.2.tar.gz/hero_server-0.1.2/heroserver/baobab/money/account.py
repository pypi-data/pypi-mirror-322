from pydantic import Field
from baobab.core.base import BaseWithTag


class Account(BaseWithTag):
    blockchain_type: str = Field(..., description="enum: stellar, eth, solana, tfchain")
    pub_key: str = Field(..., description="public key of the account")

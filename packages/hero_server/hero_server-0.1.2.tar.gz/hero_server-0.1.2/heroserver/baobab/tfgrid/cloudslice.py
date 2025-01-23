from pydantic import Field
from typing import List
from baobab.core.base import BaseWithTag, WebLink
from baobab.money.currency import CurrencyAmount


class CloudSlice(BaseWithTag):
    node_id: int = Field(
        ..., description="link to the node who is hosting this cloudslice"
    )
    cloudhour_cost: CurrencyAmount = Field(..., description="cost of 1 hour of cloud ")
    bandwidth_gb_cost: CurrencyAmount = Field(
        ..., description="cost for 1 GB of bandwidth"
    )
    storage_min_gb: int = Field(..., description="min 50GB per cloudslice")
    storage_max_gb: int
    passmark_min: int
    passmark_max: int
    aggregation_max: int = Field(
        ..., description="max nr of cloudslices which can be combined"
    )
    links_support: List[WebLink] = Field(...)
    farming_pool: int = Field(..., description="pointer to hosting pool")
    farmer: int = Field(
        ..., description="pointer to farmer if there is no hosting pool"
    )
    pubip6: bool = Field(..., description="is it possible to get pubip address (ipv6)")
    pubip4: bool = Field(..., description="is it possible to get pubip address (ipv4)")
    links_monitoring: List[WebLink] = Field(...)
    location: int = Field(..., description="link to location object")
    nft_id: int = Field(..., description="key of the NFT representing this cloudslice")

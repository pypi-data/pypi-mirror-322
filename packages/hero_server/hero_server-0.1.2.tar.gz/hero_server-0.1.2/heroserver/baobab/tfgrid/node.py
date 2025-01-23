from baobab.core.base import BaseWithTag, WebLink
from typing import List
from pydantic import Field


class Node(BaseWithTag):
    farming_pool: int = Field(..., description="pointer to hosting pool")
    farmer: int = Field(
        ..., description="pointer to farmer if there is no hosting pool"
    )
    pubip6: bool = Field(..., description="is it possible to get pubip address (ipv6)")
    pubip4: bool = Field(..., description="is it possible to get pubip address (ipv4)")
    links_monitoring: List[WebLink] = Field(...)
    location: int = Field(..., description="link to location object")
    storage_ssd_gb: int = Field(...)
    storage_hdd_gb: int = Field(...)
    passmark: int = Field(...)
    links_support: List[WebLink] = Field(...)
    uptime: int = Field(..., description="0..100")

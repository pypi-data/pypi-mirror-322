from typing import List
from pydantic import Field
from baobab.core.base import BaseWithTag, WebLink


class FarminPool(BaseWithTag):
    farmer: int = Field(
        ..., description="pointer to farmer if there is no hosting pool"
    )
    pubip6: bool = Field(..., description="is it possible to get pubip address (ipv6)")
    pubip4: bool = Field(..., description="is it possible to get pubip address (ipv4)")
    links_monitoring: List[WebLink] = Field(...)
    location: int = Field(..., description="link to location object")

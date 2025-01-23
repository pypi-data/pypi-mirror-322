from typing import List
from pydantic import Field
from baobab.core.base import Base, WebLink
from baobab.circle_model.address import PostalAddress


class Contact(Base):
    email: List[str] = Field(..., description="email addresses")
    mobile: List[str] = Field(..., description="mobile numbers")
    weblinks: List[WebLink] = Field(..., description="website urls of the company")
    address: List[PostalAddress] = Field(
        ..., description="can be more than 1 addr linked to it"
    )

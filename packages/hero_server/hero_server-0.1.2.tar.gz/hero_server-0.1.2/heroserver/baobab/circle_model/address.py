from pydantic import Field
from baobab.core.base import Base

# pub struct PostalAddress {
#     core.Base
# mut:
#     country_id string	//specify which std to use
#     street  string
#     city    string
#     state   string
#     zip     string
# }


class PostalAddress(Base):
    country_id: str = Field(..., description="specify which std to use", examples=[])
    street: str = Field(...)
    city: str = Field(...)
    zip: str = Field(...)

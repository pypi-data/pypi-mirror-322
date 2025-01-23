from pydantic import Field
from baobab.core.base import BaseWithTag


class Document(BaseWithTag):
    cat: str = Field(..., description="enum: ...")

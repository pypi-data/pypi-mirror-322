from tabella import Tabella
from pydantic import BaseModel, Field
from typing import List, Optional
from osis.db import DB
import time


# Pydantic model
class Signature(BaseModel):
    pubkey: str = Field(
        ...,
        description="The public key of the signer",
        examples=["3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX"],
    )
    content: str = Field(
        ..., description="Content that got signed", examples=["some content"]
    )
    signature: str = Field(
        ...,
        description="Signature of the content",
        examples=["5eykt4dfasdfadfadfEpY1vzqKqZKvdpHGqpCD3ZKFSs"],
    )
    time_creation: int = Field(
        default_factory=lambda: int(time.time()),
        description="Time when signature was done, in epoch",
        examples=[1711442827],
    )

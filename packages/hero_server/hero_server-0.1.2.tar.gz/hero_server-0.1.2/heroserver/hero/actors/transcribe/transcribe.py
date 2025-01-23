from tabella import Tabella
from pydantic import BaseModel, Field, validator
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
#from osis.db import DB
#from actors.mydb import db
import time
import string
import random

router = RPCRouter()
#db_cat = "circle"

class VimeoFolders(BaseModel):
    folders: str = Field(
        ...,
        description="List of folder id's in vimeo",
        examples=",".join(random.choices(string.ascii_uppercase + string.digits, k=32))
    )

@router.method()
def transcribe(folders: VimeoFolders):
    print(folders)

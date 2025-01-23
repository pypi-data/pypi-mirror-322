import requests
import os

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB
from actors.mydb import db
import time
from enum import Enum



os.environ['no_proxy'] = '*'

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

class EmailConfig(BaseModel):
    name: str = Field(..., description="Name of the mail profile", example="referral")


def struct_echo(s: EmailConfig) -> EmailConfig:
    return s
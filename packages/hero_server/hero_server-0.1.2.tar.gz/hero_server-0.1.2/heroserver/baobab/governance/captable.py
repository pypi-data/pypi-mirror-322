from typing import List
from pydantic import Field, BaseModel
from baobab.core.base import Base


struct ShareHolder {
    user        int    // if a user
    contact     int    // if not a user
    name        string
    description string
}

struct CaptablePosition {
    shareholder ShareHolder
    nrshares    int
    shareclass  string
}

struct Captable {
    positions []CaptablePosition
}

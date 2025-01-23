from typing import List, Optional
from pydantic import Field, BaseModel
from baobab.core.base import Base


class Role(BaseModel):
    """
    a role to be fulfiled by a person of a department e.g. legal, is the ownership
    """

    name: str = Field(...)
    description: str = Field(...)
    users: List[int] = Field(..., description="link to users, normally only 1")
    cat: str = Field(
        ...,
        description="enum free for what is the role defaults legal,admin,coordination,finance,engineering,sales,marketing",
    )


class Location(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    contact: int = Field(...)
    cat: str = Field(..., description="enum: anu, hq, research, sales, ...")


class Department(BaseModel):
    roles: List[Role] = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    circle_member_selection: List[int] = Field(
        ...,
        description="link to CircleMemberSelection, is way how to flexibly chose members for a department",
    )


class EntityInfo(BaseModel):
    """
    some adhoc info about a company
    """

    industry: str = Field(..., description="industry the company operates in")
    founding_year: int = Field(..., description="year the company was founded")
    nr_employees: int = Field(..., description="number of employees in the company")


class Entity(Base):
    """
    can be a company or any other structure, can represent a person who signs, unique id
    """

    parent: int = Field(
        ..., description="if this entity is 100 percent owned by the another entity"
    )
    locations: List[Location] = Field(...)
    departments: List[Department] = Field(...)
    info: Optional[EntityInfo] = Field(...)

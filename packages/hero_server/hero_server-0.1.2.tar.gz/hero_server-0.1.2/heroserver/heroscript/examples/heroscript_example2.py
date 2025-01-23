from pydantic import BaseModel, Field
from typing import Dict, Any, Type, TypeVar, List
from heroscript.heroscript import *

class Comment(BaseModel):
    description: str = Field(default="")
    
class HeroBase(BaseModel, HeroScriptMixin):
    oid: str = Field(default="",metadata={"unique": True})
    name: str = Field(min_length=2, description="Chosen name by user", example="myname",metadata={"unique": True})
    comments: List[Comment] = Field(..., description="Comment which can be attached to obj")

class User(HeroBase):
    city: str = Field(metadata={"index": True})
    age: int = Field(metadata={"index": True})
    description: str = Field(default="")

class Product(BaseModel, HeroScriptMixin):
    id: int = Field(default="",metadata={"unique": True})
    name: str = Field(metadata={"unique": True})
    price: float = Field()
    description: str = Field()
    
    
myheroscript="""

```hero
!!user.define
    oid:abc123
    name:John
    description:'
        this is a multiline

        we need to remove the
            this will stay 4 chars in

        end
    '
    age:30
    city:'New York'
    
!!product.define
    id:33
    name:aproduct
    description:'
        this is a multiline

        we need to remove the
            this will stay 4 chars in

        end
    '
    price:10.0
    
```

"""

# hs=HeroScripts(class_types={"user":User,"product":Product},content=myheroscript)
mypath="~/code/git.ourworld.tf/tfgrid/hero_research/hero/osis/heroscript/example"
hs=HeroScripts(class_types={"user":User,"product":Product},path=mypath)

objs=hs.get_objects()

for o in objs:
    myprint(o) 
    
for item in hs.heroscripts:
    print(item)
    
query = "john*"
results = hs.search(User, query)

# Print the search results
for r in results:
    # print(f"User: {r["path"]}")
    print(r)
    
from pydantic import BaseModel, Field
from typing import Dict, Any, Type, TypeVar
from heroscript.heroscript import *


class User(BaseModel, HeroScriptMixin):
    oid: str = Field()
    name: str = Field(min_length=2, description="Chosen name by user", example="myname")
    city: str = Field()
    age: int = Field()
    description: str = Field()



# Example usage
u1 = User(oid="abc123", name="John", age=30, city="New York",
          description="""
          this is a multiline
          
          we need to remove the 
              this will stay 4 chars in
          
          end
          """)

myheroscript = u1.heroscript()
print(myheroscript)

u2 = User.from_heroscript(heroscript=myheroscript)
myprint(u2)

# p1 = Product(id=1, name="Phone", price=999.99, description="A smart phone")

# product_heroscript = p1.heroscript()
# print(product_heroscript)

# p2 = Product.from_heroscript(product_heroscript)
# print(p2)
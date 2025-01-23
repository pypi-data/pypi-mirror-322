remarks: the following are instructions to create a server module in python, no need to follow url links

can you create an openrpc server based on tabella library in python

we need pydantic interfaces for the structs as they are expressed below in v structs

for pydantic we need the descriptions and default values, the pydantic as known by you is old, upgrade to the following

- parse_raw is not longer valid on e.g. Object, it needs to be model_validate_json
- json is not longer valid on e.g. Object, it needs to be model_dump_json
- we need pydantic examples in the fields

the source of our models are defined in vlang structs, the property OurTime needs to be done as an int which is epoch and the default is time.now() from python
in next code block we have an example source model

```vlang
module user

pub struct User {
pub mut:
    #the following 4 are almost always there in the spec
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *

	pubkey string //Unique key for a user, is on blockchain solana, also address where money goes example="3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX" *
	name string //chosen name by user, need to be unique on tfgrid level example=myname *
	ipaddr string //mycelium ip address  example="fe80::5f21:d7a2:5c8e:ecf0" *
	email []string //Email addresses example=info@example.com,other@email.com  *
	mobile []string //Mobile number example="+324444444" *
}


```

### use of OSIS

we use a self made library which is called OSIS which stores the data and indexes the models (its basically a key value stor + indexing)

the library is used as follows

```python
from osis.db import DB #is our own database implementation


# Create indexes (needs to be done for each object)
# oid is always there
stor.index_create("user", oid=str, pubkey=str, name=str, ipaddr=str, email=str, mobile=str,time_creation=int)


# Create the database instance
db = DB(secret="mysecretkey", index_path="/tmp/index", index_backup_path="/tmp/indexbackup")

# Set data
user_json= "..." #the data coming fromjson serialization
#is always first type of obj e.g.user, then oid then the json data, after that all index properties
user_id = db.set("user", user.oid, user_json, name=user.name, ipaddr=user.ipaddr, email=user.email, mobile=user.mobile,time_creation=user.time_creation)

# Get data (based on oid)
json_data = stor.get("user", "3a4")
print("User data:", json_data)

# Find data (can filter based on properties as known above)
users = stor.find("user", name="john*", email="myemail@info.com")
print("Users found:")
for user in users:
    print(user.oid, user.pubkey, user.name)

```

on db.set the properties are as follows

- the key (unique identifier) of the object, is the first row of the defined class (struct) in this case its the oid
- name of the object e.g. user (the category = cat)
- the data of the object
- then kwargs are the properties which need to be indexed in this case all which have \* at end of definition in the struct which defines the model

## example output script per object

example generation for user.py

```python
from tabella import Tabella
from pydantic import BaseModel, Field, EmailStr, validator
from openrpc import RPCRouter
from typing import List, Optional
from fastapi import Depends, Request
from osis.db import DB #is our own database implementation
from actors.mydb import db #is our connection to the database
import time


router = RPCRouter() //is used for the methods
db_cat="user"  #needs to be the lowercase name of the object in this case user

/////////////////
//pydantic models

#example import for signature, is object is not specified in file itself (spec, import like this)
from actors.circle.signature import Signature

#DO GENERATE THE OBJECT IF SPECIFIED IN THE SPEC FILE (V structs) and then don't import

class User(BaseModel):
    #oid is default ""
    oid: str = Field(default="",description="Unique ID for user in a circle", example="a7c")
    signatures: List[Signature] = Field(description="Signatures associated with the user")
    comments: List[str] = Field(description="List of oid's of comments linked to this story")
    #time_creation default 0
    time_creation: int = Field(default=0,description="Time when signature was created, in epoch", example=1711442827)

    pubkey: str = Field(..., description="Unique key for a user, is on blockchain solana, also address where money goes", example="3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX")
    name: str = Field(..., description="Chosen name by user, needs to be unique on tfgrid level", example="myname")
    ipaddr: str = Field(..., description="Mycelium IP address", example="fe80::5f21:d7a2:5c8e:ecf0")
    email: List[str] = Field(..., description="Email addresses", example=["info@example.com", "other@email.com"])
    mobile: List[str] = Field(..., description="Mobile numbers", example=["+324444444"])

/////////////////
//api methods


def index_create(db: DB):
    #helper function to create the index, this needs to be done for each object, in this case its for user, oid is always there as string
    db.index_create("user", oid=str, pubkey=str, name=str, ipaddr=str, email=str, mobile=str, time_creation=int)

@router.method()
def set(user User ) -> int:
    #always in set do an obj_check on db for the obj
    user=db.obj_check(user)
    json_data = req.model_dump_json()
    #we always use oid from object to set & get
    user_id = db.set("user", user.oid, json_data, name=user.name, ipaddr=user.ipaddr, email=user.email, mobile=user.mobile,time_creation=user.time_creation)
    return user_id


#REMARK: get can only have 1 input, and get is just the category and the input is first property of object we generate for
@router.method()
def get(oid str ) ->  Optional[User]:
    #we always use oid from object to set & get
    json_data = db.get("user",oid)
    if json_data:
        return User.model_validate_json(json_data)
    return None

@router.method()
def delete(oid str):
    db.delete("user",oid)


class UserFilter(BaseModel):
    pubkey: Optional[str] = None
    name: Optional[str] = None
    ipaddr: Optional[str] = None
    email: Optional[str] = None #when emails, so more than one comma separated is always allowd
    mobile: Optional[str] = None #is more than one mobile so comma separated
    from_time: Optional[int] = None
    to_time: Optional[int] = None


@router.method()
def list(args: UserFilter, ) -> List[User]:
    #code to get from UserFilter to kwargs
    args.email = [item.strip() for item in args.emails.split(',')] #because is list, comma alloweds
    args.mobile = [item.strip() for item in args.mobile.split(',')]
    kwargs = args.dict(exclude_none=True)
    if "from_time" in kwargs:
        kwargs["time_creation__gte"] = kwargs.pop("from_time")
    if "to_time" in kwargs:
        kwargs["time_creation__lte"] = kwargs.pop("to_time")
    users_json = db.find("user", **kwargs)
    users = [User.model_validate_json(result.data) for result in users_json]
    return users

```

use the example code as above, try to stay as close as possible but then for other object as will be requested at bottomn of this prompt

we then use openrpc (which is implemented by tabella) in python see example up

the aim is to generate for each object the pydantic models as well as the endpoints for our openrpc server
we will at end of this prompt specify which object to generate everything for

we create 1 file $objectname.py per object e.g. User, see how this example implementation maps to the User & Signature definition in the vstruct above

the first part generate code for the pydantic model (in the file)
in the second part you should generate the code for the api (openrpc),

note each method accepts the pydantic model as input and will use json to store in redis
how we use mode_dump_json() in stead of json() on the pydantic classes
and model_validate_json() in stead of parse_raw()

the generation for the server generates set,get,delete,list.
the get is a list, which uses the UserFilter which is based on the most relevant properties,

if there is a time (has word time) in a field, then for the list we need to filter time from_time to to_time as epoch, this way we filter all objects with time > as mentioned or < then time mentioned (to time) in filter.

- set method will accept the User object and then go to json and then store in redis as hset on hset "hero:user" with key the first element of the struct (here pubkey)
- get method will accept first property as argument, here its pubkey and return the User object, which is in redis on hset
- delete method will accept first property as argument, here its pubkey and delete the object, which is in redis on hset
- list method will accept all relevant properties as a UserFilter (they have _ at end of line) in this case: pubkey, name, ipaddr, email, mobile for object user (all have _ at end)

all the data is in the DB as defined above in OSIS

==== lets now execute:

on next prompts we will ask you to generate the file e.g. project.py for the Project object based on the struct provided, struct provided is always in Vlang format

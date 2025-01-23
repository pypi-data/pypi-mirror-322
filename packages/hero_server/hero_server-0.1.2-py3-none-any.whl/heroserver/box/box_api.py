from fastapi import APIRouter, HTTPException,Response
from pydantic import BaseModel, constr, Field
from secret.box import box_secret_set,box_get

#TODO: KRISTOF FIX

router = APIRouter()

##############POSITION

class BoxSecretSetRequest(BaseModel):
    secret: str = Field(..., description="a well chosen secret key, do never forget this key, you will loose your assets")



@router.post("/secret",description="Set your secret for your hero, will be kept for 12 hours")
async def set_secret(request: BoxSecretSetRequest):
    box_secret_set(secret=request.secret)
    return Response(content="OK", media_type="text/plain")


@router.get("/secret",description="Check if it exists.")
async def secret_check():
    b=box_get()
    return Response(content="OK", media_type="text/plain")
     

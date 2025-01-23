from fastapi import HTTPException
from cryptography.fernet import Fernet
import redis
import base64
import hashlib

#TODO: KRISTOF FIX

def box_get():
    r = redis.Redis(host='localhost', port=6379, db=0)

    key = r.get('my.secret')

    if key is None:
        raise HTTPException(status_code=404, detail="can't find my.secret in redis, needs to be set: "+name+" use secret-set to register your secret.")


    hash_digest = hashlib.sha256(key).digest()
    
    # Encode the hash digest to make it url-safe base64-encoded
    key2 = base64.urlsafe_b64encode(hash_digest)    

    try:
        f = Fernet(key2)
    except Exception as e:
        # if str(e).find("Resource Missing")>0:
        #     raise HTTPException(status_code=400, detail="Could not find account with pubkey: "+account_keypair.public_key)            
        raise HTTPException(status_code=400, detail=str(e))    

    return f


def box_secret_set(secret:str):
    r = redis.Redis(host='localhost', port=6379, db=0)

    # key = r.set('my.secret',secret)
    r.setex('my.secret', 43200,secret)  # Set the key with an expiration time of 12 hours    

    box_get()

    return "OK"

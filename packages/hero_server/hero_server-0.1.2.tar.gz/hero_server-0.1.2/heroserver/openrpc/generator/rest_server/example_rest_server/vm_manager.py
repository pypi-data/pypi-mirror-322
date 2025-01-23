from typing import Union

from fastapi import FastAPI
from vm_manager__vm_start import vm_start

app = FastAPI()

#VM WOULD BE AN OBJECT of e.g. a virtual machine description

@app.get("/$circleguid/vm_manager/vm")
def vm_get()-> VM:
    return {...}


@app.post("/$circleguid/vm_manager/vm")
def vm_set()-> bool:
    return True

@app.delete("/$circleguid/vm_manager/vm")
def vm_delete()-> bool:
    ##would use osis to delete this objecc
    return True


@app.get("/$circleguid/vm_manager/vm_start/{vm_guid}")
def vm_start(vm_guid: str) -> bool:
    vm_start(context=context,vm_guid=vm_guid)
    

from heroserver.openrpc.factory import openrpc_dict, openrpc_spec, openrpc_spec_write
from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec


def init_openrpc_dict(path: str = "") -> dict:
    """
    return openrpc dict
    """
    return openrpc_dict(path=path)


def init_openrpc_spec_write(path: str = "", dest: str = "") -> str:
    """
    parse & write the specs to the destination, the path will be ${destination}/openrpc_spec.json" and .../openrpc_spec.yaml"
    """
    return openrpc_spec_write(path=path, dest=dest)


def init_openrpc_spec(path: str = "") -> OpenRPCSpec:
    """
    return openrpc object
    """
    return openrpc_spec(path=path)

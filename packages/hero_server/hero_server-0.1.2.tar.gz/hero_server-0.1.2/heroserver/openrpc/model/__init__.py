import json

import yaml  # type: ignore

from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec

# def decode_openrpc(yaml_string: str) -> dict:
#     # TODO:
#     pass


# def encode_openrpc(openrpc_object: dict) -> str:
#     # TODO:
#     pass


def decode_openrpc_yaml(yaml_string: str) -> OpenRPCSpec:
    # Parse YAML string into a Python dict and then convert it into an OpenRPCObject using Pydantic
    data = yaml.safe_load(yaml_string)
    return OpenRPCSpec.load(data)


def encode_openrpc_yaml(openrpc_object: OpenRPCSpec) -> str:
    # Convert the OpenRPCObject instance to a dictionary and then dump it to a YAML string
    return yaml.dump(openrpc_object.__dict__, sort_keys=False, allow_unicode=True)


def decode_openrpc_json(json_string: str) -> OpenRPCSpec:
    d = json.loads(json_string)
    return OpenRPCSpec.load(d)


def encode_openrpc_json(openrpc_object: OpenRPCSpec) -> str:
    # Convert the OpenRPCObject instance to a dictionary and then dump it to a JSON string
    return json.dumps(openrpc_object, indent=4)


# check that the dict is well formatted
def check(openrpc_spec: dict) -> bool:
    # todo, try to load the dict in openrpc object
    json_spec = json.dumps(openrpc_spec)
    try:
        decode_openrpc_json(json_spec)
    except:
        return False
    return True


if __name__ == "__main__":
    from heroserver.openrpc.parser.cleaner import load
    from heroserver.openrpc.parser.parser import parser

    openrpc_spec = parser(load("/root/code/git.ourworld.tf/projectmycelium/hero_server/lib/openrpclib/parser/examples"))

    print(check(openrpc_spec))

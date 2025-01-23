import json
import os

import yaml  # type: ignore

from heroserver.openrpc.model.openrpc_spec import (
    OpenRPCSpec,
)
from heroserver.openrpc.parser.parser import parser


def openrpc_spec_write(path: str = "", dest: str = "") -> str:
    """
    parse & write the specs
    dest is the path where we write the openrpc specs
    returns filename = f"{dest}/openrpc_spec.json"
    """
    data = openrpc_dict(path=path)

    out = json.dumps(data, indent=2)
    # print(out)

    dest = os.path.expanduser(dest)
    os.makedirs(dest, exist_ok=True)

    filename = f"{dest}/openrpc_spec.json"
    # Write the spec to the file
    with open(filename, "w") as f:
        f.write(out)
    print(f"OpenRPC specification (JSON) has been written to: {filename}")

    yaml_filename = f"{dest}/openrpc_spec.yaml"
    with open(yaml_filename, "w") as f:
        yaml.dump(data, f, sort_keys=False)
    print(f"OpenRPC specification (YAML) has been written to: {yaml_filename}")

    return filename


def openrpc_spec(path: str = "") -> OpenRPCSpec:
    """
    return openrpc object starting from spec path
    this is our python representation of OpenRPCSpec
    """
    data = openrpc_dict(path=path)

    spec_object = OpenRPCSpec.load(data)

    return spec_object


def openrpc_dict(path: str = "") -> dict:
    """
    return openrpc dict starting from spec path
    """
    data = parser(path=path)

    return data

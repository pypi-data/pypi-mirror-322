import os
from pathlib import Path
from typing import Dict, Optional

from heroserver.openrpc.factory import openrpc_dict, openrpc_spec, openrpc_spec_write
from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec


class OpenRPCFactory:
    def __init__(self, generation_path: str, spec_path: str):
        """
        Initialize the OpenRPCFactory with a generation path and a spec path.

        :param generation_path: The path where the generation will occur.
        :param spec_path: The path to the OpenRPC specification (in vlang format).
        """
        import os.path

        self.actors: Dict[str, OpenRPCActor] = {}
        self.generation_path: str = os.path.expanduser(generation_path)
        self.spec_path: str = os.path.expanduser(spec_path)

    def add_actor(self, actor: "OpenRPCActor"):
        self.actors[actor.name] = actor

    def get_actor(self, name: str) -> Optional["OpenRPCActor"]:
        return self.actors.get(name)

    def remove_actor(self, name: str) -> None:
        self.actors.pop(name, None)

    def scan(self):
        for subdir in os.listdir(self.spec_path):
            subdir_path = os.path.join(self.spec_path, subdir)
            if os.path.isdir(subdir_path):
                actor = OpenRPCActor(name=subdir, path_ourspec=subdir_path, parent=self)
                self.add_actor(actor)


class OpenRPCActor:
    def __init__(self, name: str, path_ourspec: str, parent: OpenRPCFactory):
        self.name: str = name
        self.path_ourspec: str = path_ourspec  # the directory where we parse & generate
        self.path_openrpc: str = os.path.join(parent.generation_path, self.name)  # the file which represents openrpc spec
        self.parent = parent

        self.openrpc_spec: OpenRPCSpec = openrpc_spec(path=path_ourspec)

    def openrpc_dict(self) -> dict:
        return openrpc_dict(path=self.path_ourspec)

    def openrpc_spec_write(self) -> dict:
        return openrpc_spec_write(path=self.path_ourspec, dest=self.path_openrpc)

    def openrpc_spec_yaml_path(self) -> str:
        yaml_path = os.path.join(self.path_openrpc, "openrpc_spec.yaml")
        if not os.path.exists(yaml_path):
            self.openrpc_spec_write()
        return yaml_path

    def openrpc_spec_json_path(self) -> str:
        json_path = os.path.join(self.path_openrpc, "openrpc_spec.json")
        if not os.path.exists(json_path):
            self.openrpc_spec_write()
        return json_path

    def generate_rest_server(self):
        from heroserver.openrpc.generator.rest_server.python.rest_server_generator import RestServerGenerator

        rest_server_generator = RestServerGenerator(self.openrpc_spec, Path(self.path_openrpc))
        rest_server_generator.generate()


def new(generation_path: str, spec_path: str) -> OpenRPCFactory:
    """
    Create a new OpenRPCFactory and return OpenRPCActors, starting from a path.

    :param generation_path: The path where the generation will occur.
    :param spec_path: The path to the OpenRPC specification.
    :return: An instance of OpenRPCFactory with actors initialized.
    """
    factory = OpenRPCFactory(generation_path=generation_path, spec_path=spec_path)
    factory.scan()
    return factory


# Usage example:
# spec = OpenRPCSpec(...)  # Create an OpenRPCSpec instance
# actor = OpenRPCActor("MyActor", "/path/to/actor", spec, "/path/to/openrpc.json")
# actors = OpenRPCActors()
# actors.add_actor(actor)

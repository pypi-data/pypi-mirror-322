import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec

script_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(script_dir))


class ServerGenerator:
    def __init__(self, spec: OpenRPCSpec, dir: Path):
        self.spec = spec
        self.dir = dir

        self.server_template = env.get_template("templates/server.jinja")

    def generate(self):
        self.dir.mkdir(parents=True, exist_ok=True)

        self.generate_server()
        self.generate_models()
        self.generate_methods()

    def generate_server(self):
        code = self.server_template.render()
        server_file_path = self.dir.joinpath("server.v")

        with open(server_file_path, "w") as file:
            file.write(f"{code}")

    def generate_models():
        pass

    def generate_methods():
        pass


if __name__ == "__main__":
    from heroserver.openrpc.parser.parser import parser

    # from heroserver.openrpc.generator.model_generator import ModelGenerator

    data = parser(path="/root/code/git.ourworld.tf/hero_server/generatorexamples/mycelium_openrpc.yaml")

    spec_object = OpenRPCSpec.load(data)
    server_generator = ServerGenerator(spec_object, Path("/tmp/server3"))
    server_generator.generate()

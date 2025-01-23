import os
from pathlib import Path
from typing import Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader

from heroserver.openrpc.generator.actor.vlang.vlang_code_generator import VlangGenerator
from heroserver.openrpc.generator.model_generator import ModelGenerator
from heroserver.openrpc.model.common import ContentDescriptorObject, ReferenceObject
from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec

script_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(script_dir))


class RestServerGenerator:
    def __init__(
        self,
        spec: OpenRPCSpec,
        dir: Path,
    ) -> None:
        self.lang_code_generator = VlangGenerator()
        self.model_generator = ModelGenerator(spec, VlangGenerator())
        self.spec = spec
        self.dir = dir
        self.crud_methods_template = env.get_template("templates/crud_methods.jinja")
        self.internal_crud_methods_template = env.get_template("templates/internal_crud_methods.jinja")
        self.imports_template = env.get_template("templates/imports.jinja")
        self.actor_method_template = env.get_template("templates/actor_method.jinja")
        self.internal_actor_method_template = env.get_template("templates/internal_actor_method.jinja")
        self.server_template = env.get_template("templates/server.jinja")

    def generate(self):
        self.dir.mkdir(parents=True, exist_ok=True)

        self.generate_models()
        self.generate_crud()
        self.generate_internal_actor_methods()
        self.generate_openapi()
        self.generate_server()

        print(f"Generated API code has been written to {self.dir}")

    def generate_server(self):
        imports = self.imports_template.render(import_vweb=True)
        code = self.server_template.render()

        path = self.dir.joinpath("server.v")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{code}")

    def generate_openapi(self):
        imports = self.imports_template.render(import_vweb=True)
        methods = ""
        for path_str in self.model_generator.spec.get_root_objects().keys():
            object = self.model_generator.processed_objects[path_str]
            if object["code"] == "":
                continue

            type_name = object["name"]
            variable_name = type_name.lower()
            methods += self.crud_methods_template.render(variable_name=variable_name, type_name=type_name) + "\n\n"

        for method in self.spec.methods:
            if any(method.name.endswith(end) for end in ["get", "set", "delete"]):
                continue

            params: Dict[str, str] = {}
            for param in method.params:
                params[param.name] = self.model_generator.jsonschema_to_type(["methods", method.name, "params", param.name], param.schema)

            return_type = self.method_result_return_type(["methods", method.name, "result"], method.result)

            function_name = method.name.lower().replace(".", "_")
            methods += (
                self.actor_method_template.render(
                    rest_server_generator=self,
                    function_name=function_name,
                    method_params=params,
                    method_result=return_type,
                )
                + "\n\n"
            )

        path = self.dir.joinpath("open_api.v")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{methods}")

    def generate_models(self):
        imports = self.imports_template.render()
        code = self.model_generator.generate_models()
        path = self.dir.joinpath("models.v")

        with open(path, "w") as file:
            file.write(f"{imports}\n\n{code}\n")

    def generate_crud(self):
        imports = self.imports_template.render(import_models=True)
        methods = ""
        for path_str in self.model_generator.spec.get_root_objects().keys():
            object = self.model_generator.processed_objects[path_str]
            if object["code"] == "":
                continue

            type_name = object["name"]
            variable_name = type_name.lower()
            methods += self.internal_crud_methods_template.render(variable_name=variable_name, type_name=type_name) + "\n\n"

        path = self.dir.joinpath("crud.v")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{methods}")

    def generate_internal_actor_methods(self):
        imports = self.imports_template.render(import_models=True)
        for method in self.spec.methods:
            function_name = method.name.lower().replace(".", "_") + "_internal"
            file_path = self.dir.joinpath(f"{function_name}.v")
            if file_path.exists():
                continue

            if any(method.name.endswith(end) for end in ["get", "set", "delete"]):
                continue

            params: Dict[str, str] = {}
            for param in method.params:
                params[param.name] = self.model_generator.jsonschema_to_type(["methods", method.name, "params", param.name], param.schema)

            return_type = self.method_result_return_type(["methods", method.name, "result"], method.result)

            code = self.internal_actor_method_template.render(
                rest_server_generator=self,
                function_name=function_name,
                method_params=params,
                method_result=return_type,
            )

            with open(file_path, "w") as file:
                file.write(f"{imports}\n\n{code}")

    def get_method_params(self, method_params: Dict[str, str]) -> str:
        return ", ".join([f"{param_name} {param_type}" for param_name, param_type in method_params.items()])

    def method_result_return_type(
        self,
        path: List[str],
        method_result: Optional[Union[ContentDescriptorObject, ReferenceObject]],
    ) -> str:
        if not method_result:
            type_name = ""

        if isinstance(method_result, ContentDescriptorObject):
            schema = method_result.schema
            type_name = self.model_generator.jsonschema_to_type(path, schema)

        elif isinstance(method_result, ReferenceObject):
            type_name = self.model_generator.jsonschema_to_type(path, method_result)

        return type_name


if __name__ == "__main__":
    from heroserver.openrpc.generator.model_generator import ModelGenerator
    from heroserver.openrpc.parser.parser import parser

    data = parser(path="/root/code/git.ourworld.tf/projectmycelium/hero_server/generatorexamples/example1/specs/storymanager")

    spec_object = OpenRPCSpec.load(data)
    server_generator = RestServerGenerator(spec_object, Path("/tmp/rest3"))
    server_generator.generate()

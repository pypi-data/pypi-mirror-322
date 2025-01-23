import os
from pathlib import Path
from typing import Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader

from heroserver.openrpc.generator.code.python.python_code_generator import PythonCodeGenerator
from heroserver.openrpc.generator.model.model_generator import ModelGenerator

# Fix the issue by ensuring that the 'object' variable is properly defined and has the expected attributes.
# The following code will ensure that 'object' is a valid SchemaObject before calling 'print_items'.
from heroserver.openrpc.model.common import ContentDescriptorObject, ReferenceObject, SchemaObject
from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec
from heroserver.openrpc.parser.parser import parser

script_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(script_dir))


class RestServerGenerator:
    def __init__(
        self,
        spec: OpenRPCSpec,
        dir: Path,
    ) -> None:
        if not isinstance(spec, OpenRPCSpec):
            raise TypeError(f"Expected spec to be of type OpenRPCSpec, got {type(spec)}")
        if not isinstance(dir, Path):
            raise TypeError(f"Expected dir to be of type Path, got {type(dir)}")

        self.model_generator = ModelGenerator(spec, PythonCodeGenerator())
        self.spec = spec
        self.dir = dir
        self.crud_methods_template = env.get_template("templates/crud_methods.jinja")
        self.internal_crud_methods_template = env.get_template("templates/internal_crud_methods.jinja")
        self.internal_crud_mock_methods_template = env.get_template("templates/internal_crud_mock_methods.jinja")
        self.imports_template = env.get_template("templates/imports.jinja")
        self.actor_method_template = env.get_template("templates/actor_method.jinja")
        self.internal_actor_method_template = env.get_template("templates/internal_actor_method.jinja")
        self.server_template = env.get_template("templates/server.jinja")

    def generate(self):
        self.dir.mkdir(parents=True, exist_ok=True)

        self.generate_models()
        self.generate_crud()
        self.generate_mock_crud()
        self.generate_internal_actor_methods()
        self.generate_openapi()
        self.generate_openapi_mock()
        self.generate_server()

        print(f"Generated API code has been written to {self.dir}")

    def generate_server(self):
        code = self.server_template.render()

        path = self.dir.joinpath("server.py")
        with open(path, "w") as file:
            file.write(code)

    def generate_openapi(self):
        imports = self.imports_template.render(import_crud=True, import_models=True)
        app_init = "app = FastAPI()\n\n"
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
            imports += f"from {function_name}_internal import {function_name}_internal\n"
            methods += (
                self.actor_method_template.render(
                    rest_server_generator=self,
                    function_name=function_name,
                    method_params=params,
                    method_result=return_type,
                )
                + "\n\n"
            )

        path = self.dir.joinpath("open_api.py")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{app_init}\n\n{methods}")

    def generate_openapi_mock(self):
        imports = self.imports_template.render(mock=True, import_crud=True, import_models=True)
        app_init = "app = FastAPI()\n\n"
        methods = ""
        for path_str in self.model_generator.spec.get_root_objects().keys():
            object = self.model_generator.processed_objects[path_str]
            if object["code"] == "":
                continue

            type_name = object["name"]
            variable_name = type_name.lower()
            methods += self.crud_methods_template.render(mock=True, variable_name=variable_name, type_name=type_name) + "\n\n"

        for method in self.spec.methods:
            if any(method.name.endswith(end) for end in ["get", "set", "delete"]):
                continue

            params: Dict[str, str] = {}
            for param in method.params:
                params[param.name] = self.model_generator.jsonschema_to_type(["methods", method.name, "params", param.name], param.schema)

            return_type = self.method_result_return_type(["methods", method.name, "result"], method.result)

            function_name = method.name.lower().replace(".", "_")
            imports += f"from {function_name}_internal import {function_name}_internal\n"
            methods += (
                self.actor_method_template.render(
                    mock=True,
                    rest_server_generator=self,
                    function_name=function_name,
                    method_params=params,
                    method_result=return_type,
                )
                + "\n\n"
            )

        path = self.dir.joinpath("open_api_mock.py")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{app_init}\n\n{methods}")

    def generate_models(self):
        imports = self.imports_template.render()
        code = self.model_generator.generate_models()
        path = self.dir.joinpath("models.py")

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

        path = self.dir.joinpath("crud.py")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{methods}")

    def generate_mock_crud(self):
        imports = self.imports_template.render(import_models=True)
        imports += "from heroserver.openrpc.tools import create_example_object"
        methods = ""
        for path_str in self.model_generator.spec.get_root_objects().keys():
            object = self.model_generator.spec.get_root_objects()[path_str]

            if isinstance(object, SchemaObject):
                print_items(object)

            object = self.model_generator.processed_objects[path_str]
            if object["code"] == "":
                continue

            type_name = object["name"]
            variable_name = type_name.lower()

            methods += self.internal_crud_mock_methods_template.render(variable_name=variable_name, type_name=type_name) + "\n\n"

        path = self.dir.joinpath("crud_mock.py")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{methods}")

    def generate_internal_actor_methods(self):
        imports = self.imports_template.render(import_models=True)
        for method in self.spec.methods:
            function_name = method.name.lower().replace(".", "_") + "_internal"
            file_path = self.dir.joinpath(f"{function_name}.py")
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
        return ", ".join([f"{param_name}: {param_type}" for param_name, param_type in method_params.items()])

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


def print_items(schema_object, depth=0):
    print(f"prito {schema_object.items}")
    indent = "    " * depth
    if isinstance(schema_object.items, list):
        for item in schema_object.items:
            print(f"{indent}Item: {item}")
            if isinstance(item, SchemaObject):
                print_items(item, depth + 1)
            print(f"{indent}Example: {item.example}")
    elif isinstance(schema_object.items, SchemaObject):
        print(f"{indent}Item: {schema_object.items}")
        print_items(schema_object.items, depth + 1)
        print(f"{indent}Example: {schema_object.items.example}")


if __name__ == "__main__":
    data = parser(path="~/code/git.ourworld.tf/hero/hero_server_python/baobabspecs")

    spec_object = OpenRPCSpec.load(data)
    server_generator = RestServerGenerator(spec_object, Path("/tmp/rest2"))
    server_generator.generate()

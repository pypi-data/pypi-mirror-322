import json
import os
from typing import Any, Dict, List
from urllib.parse import ParseResult

import inflect
from jinja2 import Environment, FileSystemLoader
from heroserver.openrpc.generator.lang_code_generator import LangCodeGenerator, PropertyInfo

from heroserver.openrpc.model.common import (
    ReferenceObject,
    SchemaObject,
)
from heroserver.openrpc.model.methods import MethodObject
from heroserver.openrpc.model.openrpc_spec import (
    OpenRPCSpec,
)

script_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(script_dir))
inflector = inflect.engine()


class GolangCodeGenerator(LangCodeGenerator):
    def __init__(self) -> None:
        self.struct_template = env.get_template("templates/struct.jinja")
        self.methods_template = env.get_template("templates/methods.jinja")
        self.pre_template = env.get_template("templates/pre.jinja")

    def generate_imports(self) -> str:
        return self.pre_template.render(
            package_name="rpcclient",
            imports=[
                "net/http",
                "github.com/mitchellh/mapstructure",
                "encoding/json",
                "bytes",
                "fmt",
                "io",
            ],
        )

    def generate_object(
        self,
        type_name: str,
        properties: Dict[str, PropertyInfo],
    ):
        return self.struct_template.render(generator=self, type_name=type_name, properties=properties)

    def generate_method(
        self,
        method_spec: MethodObject,
        url: ParseResult,
        params: Dict[str, str],
        return_type: str,
    ) -> str:
        function_name = self.get_camel_case_name(method_spec.name)
        method_name = method_spec.name
        method_result = self.type_to_method_result(return_type)
        method_description = ""
        if method_spec.description:
            method_description = method_spec.description.replace("'", " ")

        method_example = ""
        if method_spec.examples and len(method_spec.examples) > 0:
            method_example = json.dumps(method_spec.examples[0], indent=4)

        method_code = self.methods_template.render(
            generator=self,
            url=url.geturl(),
            function_name=function_name,
            method_name=method_name,
            method_params=params,
            method_result=method_result,
            return_type=return_type,
            method_description=method_description,
            method_example=method_example,
        )

        return method_code

    def string_primitive(self) -> str:
        return "string"

    def integer_primitive(self) -> str:
        return "int64"

    def number_primitive(self) -> str:
        return "float64"

    def null_primitive(self) -> str:
        return "nil"

    def bool_primitive(self) -> str:
        return "bool"

    def array_of_type(self, type_name: str) -> str:
        return f"[]{type_name}"

    def generate_multitype(self, types: List[str]) -> str:
        if len(types) > 2:
            raise Exception("only a type and null are supported with anyOf/allOf keyword")

        if len(types) == 1:
            return types[0]

        if types[0] == "nil":
            return f"*{types[1]}"
        if types[1] == "nil":
            return f"*{types[0]}"

        raise Exception("only a type and null are supported with anyOf/allOf keyword")

    def encapsulate_types(self, path: List[str], types: List[SchemaObject | ReferenceObject]) -> str:
        raise Exception("no support for allOf keyword")

    def generate_enum(self, enum: List[Any], type_name: str) -> str:
        if all(isinstance(elem, str) for elem in enum):
            return self.string_primitive()

        elif all(isinstance(elem, int) for elem in enum):
            return self.integer_primitive()

        else:
            raise Exception(f"failed to generate enum code for: {enum}")

    def type_to_method_result(self, type_name: str) -> str:
        method_result = "error"
        if len(type_name) > 0 and type_name != "nil":
            method_result = f"({type_name}, error)"

        return method_result

    def is_primitive(self, type: str) -> bool:
        return type in ["int64", "float64", "int", "bool", "string"]

    def is_array(self, type: str) -> bool:
        return type.startswith("[]")

    def get_method_params(self, method_params: Dict[str, str]) -> str:
        return ", ".join([f"{param_name} {param_type}" for param_name, param_type in method_params.items()])

    def get_camel_case_name(self, method_name: str) -> str:
        return "".join([item.title() for item in method_name.split("_")])

    def get_default_return_with_error(self, return_type: str, error_statement: str) -> str:
        if return_type == "nil":
            return error_statement

        if return_type == "string":
            return f'"", {error_statement}'

        if return_type == "bool":
            return f"false, {error_statement}"

        if return_type == "float64" or return_type == "int64":
            return f"0, {error_statement}"

        return f"{return_type}{{}}, {error_statement}"


# main()
if __name__ == "__main__":
    from heroserver.openrpc.generator.generator import ClientGenerator
    from heroserver.openrpc.parser.parser import parser

    data = parser(path="/root/code/git.ourworld.tf/projectmycelium/hero_server/generatorexamples/example1/specs/storymanager")

    spec_object = OpenRPCSpec.load(data)
    golang_code_generator = GolangCodeGenerator()
    generator = ClientGenerator(
        spec_object,
        golang_code_generator,
        "/tmp/go_client_new.go",
    )

    generator.generate_client()

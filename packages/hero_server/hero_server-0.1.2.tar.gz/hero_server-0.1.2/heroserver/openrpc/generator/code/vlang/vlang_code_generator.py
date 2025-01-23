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


class VlangGenerator(LangCodeGenerator):
    def __init__(self) -> None:
        self.struct_template = env.get_template("templates/struct.jinja")
        self.enum_template = env.get_template("templates/enum.jinja")
        self.methods_template = env.get_template("templates/methods.jinja")
        self.pre_template = env.get_template("templates/pre.jinja")

    def generate_imports(self) -> str:
        return self.pre_template.render()

    def generate_object(
        self,
        type_name: str,
        properties: Dict[str, PropertyInfo],
    ):
        return self.struct_template.render(type_name=type_name, properties=properties)

    def generate_method(
        self,
        method_spec: MethodObject,
        url: ParseResult,
        params: Dict[str, str],
        return_type: str,
    ) -> str:
        function_name = method_spec.name.lower().replace(".", "_")
        method_name = method_spec.name
        method_result = self.type_to_method_result(return_type)
        method_description = ""
        if method_spec.description:
            method_description = method_spec.description.replace("'", " ")

        method_example = ""
        if method_spec.examples and len(method_spec.examples) > 0:
            method_example = json.dumps(method_spec.examples[0], indent=4)

        method_code = self.methods_template.render(
            vlang_code_generator=self,
            base_url=f"{url.scheme}://{url.netloc}",
            url_path=url.path,
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
        return "i64"

    def number_primitive(self) -> str:
        return "f64"

    def null_primitive(self) -> str:
        return "none"

    def bool_primitive(self) -> str:
        return "bool"

    def array_of_type(self, type_name: str) -> str:
        return f"[]{type_name}"

    def generate_multitype(self, types: List[str]) -> str:
        if len(types) > 2:
            raise Exception("only a type and null are supported with anyOf/allOf keyword")

        if len(types) == 1:
            return types[0]

        if types[0] == "none":
            return f"?{types[1]}"
        if types[1] == "none":
            return f"?{types[0]}"

        raise Exception("only a type and null are supported with anyOf/allOf keyword")

    def encapsulate_types(self, path: List[str], types: List[SchemaObject | ReferenceObject]) -> str:
        raise Exception("no support for allOf keyword")

    def generate_enum(self, enum: List[Any], type_name: str) -> str:
        if all(isinstance(elem, str) for elem in enum):
            # enum of strings
            return self.enum_template.render(
                enum=enum,
                type_name=type_name,
                number_to_words=inflector.number_to_words,
            )

        elif all(isinstance(elem, int) for elem in enum):
            # enum of integers
            return self.enum_template.render(
                is_integer=True,
                enum=enum,
                type_name=type_name,
                number_to_words=inflector.number_to_words,
            )

        else:
            raise Exception(f"failed to generate enum code for: {enum}")

    def type_to_method_result(self, type_name: str) -> str:
        if type_name == "none":
            type_name = ""

        if type_name.startswith("?"):
            type_name = type_name[1:]

        return "!" + type_name

    def is_primitive(self, type: str) -> bool:
        return type in ["u64", "f64", "i64", "int", "bool", "string"]

    def is_vlang_array(self, type: str) -> bool:
        return type.startswith("[]")

    def get_method_params(self, method_params: Dict[str, str]) -> str:
        return ", ".join([f"{param_name} {param_type}" for param_name, param_type in method_params.items()])


# main()
if __name__ == "__main__":
    from heroserver.openrpc.generator.generator import ClientGenerator
    from heroserver.openrpc.parser.parser import parser

    data = parser(path="~/code/git.ourworld.tf/projectmycelium/hero_server/lib/openrpclib/parser/examples")

    spec_object = OpenRPCSpec.load(data)
    vlang_code_generator = VlangGenerator()
    generator = ClientGenerator(
        spec_object,
        vlang_code_generator,
        "/tmp/v_client_new.v",
    )

    generator.generate_client()

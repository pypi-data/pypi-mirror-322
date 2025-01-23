import json
import os
from typing import Any, Dict, List
from urllib.parse import ParseResult

import inflect
from jinja2 import Environment, FileSystemLoader

from heroserver.openrpc.generator.code.lang_code_generator import LangCodeGenerator, PropertyInfo
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

STRING_PRIMITIVE = "str"
INT_PRIMITIVE = "int"
FLOAT_PRIMITIVE = "float"
BOOL_PRMITIVE = "bool"
NONE_PRIMITIVE = "None"


class PythonCodeGenerator(LangCodeGenerator):
    def __init__(self) -> None:
        self.class_template = env.get_template("templates/class.jinja")
        self.enum_template = env.get_template("templates/enum.jinja")
        self.method_template = env.get_template("templates/method.jinja")
        self.pre_template = env.get_template("templates/pre.jinja")

    def generate_imports(self) -> str:
        return self.pre_template.render()

    def generate_object(
        self,
        type_name: str,
        properties: Dict[str, PropertyInfo],
    ):
        # for name, info in properties.items():
        #     info["load_code"] = self.generate_load_code(name, info['type'], 'data', f'data["{name}"]')

        return self.class_template.render(python_code_generator=self, class_name=type_name, properties=properties)

    def generate_load_code(self, name: str, type_name: str, data_source: str, load_param: str) -> str:
        if type_name.startswith("Optional"):
            type_name = type_name.removeprefix("Optional[").removesuffix("]")
            return f'({self.generate_load_code(name, type_name, data_source)} if "{name}" in {data_source} else None)'

        if type_name.startswith("List"):
            type_name = type_name.removeprefix("List[").removesuffix("]")
            if self.is_primitive(type_name):
                return f'{data_source}.get("{name}")'
            return f'[{self.generate_load_code(name, type_name, data_source, 'item')} for item in {data_source}.get("{name}", [])]'

        if self.is_primitive(type_name):
            return f'{data_source}.get("{name}")'

        return f"{type_name}.load({load_param})"

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
        method_description = method_description.replace("\n", "\n# ")

        method_example = ""
        if method_spec.examples and len(method_spec.examples) > 0:
            method_example = json.dumps(method_spec.examples[0], indent=4)
        method_example.replace("\n", "\n#")

        method_code = self.method_template.render(
            python_code_generator=self,
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
        return STRING_PRIMITIVE

    def integer_primitive(self) -> str:
        return INT_PRIMITIVE

    def number_primitive(self) -> str:
        return FLOAT_PRIMITIVE

    def null_primitive(self) -> str:
        return NONE_PRIMITIVE

    def bool_primitive(self) -> str:
        return BOOL_PRMITIVE

    def array_of_type(self, type_name: str) -> str:
        return f"List[{type_name}]"

    def generate_multitype(self, types: List[str]) -> str:
        if len(types) > 2:
            raise Exception("only a type and null are supported with anyOf/allOf keyword")

        if len(types) == 1:
            return types[0]

        if types[0] == NONE_PRIMITIVE:
            return f"Optional[{types[1]}]"
        if types[1] == NONE_PRIMITIVE:
            return f"Optional[{types[0]}]"

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
        return type_name

    def get_method_params(self, method_params: Dict[str, str]) -> str:
        return ", ".join([f"{param_name}: {param_type}" for param_name, param_type in method_params.items()])

    def is_primitive(self, type_name: str) -> bool:
        return type_name in [STRING_PRIMITIVE, INT_PRIMITIVE, FLOAT_PRIMITIVE, BOOL_PRMITIVE] or any(
            type_name.startswith(end) for end in ["List", "Optional", "Union"]
        )

    def get_pydantic_field_params(self, prop_info: PropertyInfo) -> str:
        field_str = ""
        if prop_info.type_name.startswith("Optional"):
            field_str = "None"
        else:
            field_str = "..."

        if prop_info.description:
            field_str += f', description="{prop_info.description}"'

        if prop_info.example:
            if isinstance(prop_info.example, str):
                example_formatted = f'"{prop_info.example}"'
            else:
                example_formatted = prop_info.example
            field_str += f", examples=[{example_formatted}]"

        return f"Field({field_str})"


# main()
if __name__ == "__main__":
    import yaml

    from heroserver.openrpc.generator.generator import ClientGenerator

    with open("/root/code/git.ourworld.tf/projectmycelium/hero_server/generatorexamples/mycelium_openrpc.yaml", "r") as file:
        data = yaml.safe_load(file)
        # print(data)
        spec_object = OpenRPCSpec.load(data)
        python_code_generator = PythonCodeGenerator()
        generator = ClientGenerator(
            spec_object,
            python_code_generator,
            "/tmp/python_client.py",
        )

        generator.generate_client()

from typing import Dict, List, Optional, Union
from urllib.parse import urlparse

from heroserver.openrpc.generator.code.lang_code_generator import LangCodeGenerator
from heroserver.openrpc.generator.model.model_generator import ModelGenerator

from heroserver.openrpc.model.common import (
    ContentDescriptorObject,
    ReferenceObject,
)
from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec


class ClientGenerator:
    def __init__(
        self,
        spec: OpenRPCSpec,
        lang_code_generator: LangCodeGenerator,
        output_file: str,
    ) -> None:
        self.spec = spec
        self.model_generator = ModelGenerator(spec, lang_code_generator)
        self.lang_code_generator = lang_code_generator
        self.output_file = output_file

    def generate_client(self):
        code_pre = self.lang_code_generator.generate_imports()
        code_models = self.model_generator.generate_models()
        code_methods = self.generate_methods()

        # Write the generated code to a file
        with open(self.output_file, "w") as file:
            file.write(code_pre)
            file.write("\n")
            file.write(code_models)
            file.write("\n")
            file.write(code_methods)

        print(f"Generated API code has been written to {self.output_file}")

    def generate_methods(self):
        servers = self.spec.servers
        base_url = "http://localhost:8000"
        if servers:
            base_url = servers[0].url

        url = urlparse(base_url)
        methods = []
        for method_spec in self.spec.methods:
            params: Dict[str, str] = {}
            for param in method_spec.params:
                params[param.name] = self.model_generator.jsonschema_to_type(
                    ["methods", method_spec.name, "params", param.name],
                    param.schema,
                )

            return_type = self.method_result_return_type(["methods", method_spec.name, "result"], method_spec.result)
            methods.append(self.lang_code_generator.generate_method(method_spec, url, params, return_type))

        return "\n\n".join(methods)

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

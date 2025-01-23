from openapi_python_client.schema import OpenAPI

import json
import yaml

from generator.server.vlang.vlang import VlangCodeGenerator

class OpenApiCodeGenerator:
    def __init__(self, lang: str, spec_file: str, output_dir: str):
        self.lang = lang
        self.spec_file = spec_file
        self.output_dir = output_dir

    def _read_file(self):
        """
        Read the OpenAPI spec file.
        """
        if self.spec_file.endswith(".json"):
            with open(self.spec_file, "r") as file:
                return file.read()  # Return raw JSON string
        elif self.spec_file.endswith(".yaml"):
            with open(self.spec_file, "r") as file:
                # Convert YAML to JSON string for compatibility
                return json.dumps(yaml.safe_load(file))
        else:
            raise ValueError("Unsupported file format")


    def generate(self):
        """
        Main generation logic for code based on the OpenAPI spec.
        """
        file_content = self._read_file()
        openapi = OpenAPI.model_validate_json(file_content)
        if self.lang == "vlang":
            vlang_code_generator = VlangCodeGenerator(
                python_code=openapi, output_dir=self.output_dir
            )
            vlang_code_generator.generate()
        elif self.lang == "python":
            print("Python code generation not implemented yet.")


if __name__ == "__main__":
    s = OpenApiCodeGenerator(
        lang="vlang",
        spec_file="/home/thunder/work/codescalers/github/hero_server_python/lib/openapi/schema.json",
        output_dir="./output"
    )
    s.generate()

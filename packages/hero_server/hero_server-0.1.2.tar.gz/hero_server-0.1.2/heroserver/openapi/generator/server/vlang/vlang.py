from openapi_python_client.schema import OpenAPI, Schema, Reference
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any

import os


script_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(script_dir))

class VlangCodeGenerator:
    def __init__(self, python_code: OpenAPI, output_dir: str) -> None:
        self.python_code = python_code
        self.output_dir = output_dir
        self.struct_template = env.get_template("templates/struct.jinja")

    def generate(self):
        """
        Main generation method to create V code.
        """
        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        structs = self._generate_structs()
        print('structs: ', structs)
        # methods = self._generate_methods()

        # # Combine structs and methods into one file
        vlang_code = structs
        output_file = f"{self.output_dir}/generated.v"

        # Write to file
        with open(output_file, "w") as file:
            file.write(vlang_code)
        print(f"Vlang code generated at {output_file}")

    def _generate_struct(self, struct_name: str, scheme: Schema | Reference) -> str:
        properties = {}
        code = ""

        for field_name, field in scheme.properties.items():  # type: ignore
            v_type = self._convert_type(field.type)  # type: ignore
            
            if field.type == 'object':  # type: ignore
                # Capitalize each part of the field name and create a nested struct name
                nested_struct_name = ''.join(part.capitalize() for part in field_name.split("_"))
                
                # Generate the struct for the nested object
                code += self._generate_struct(struct_name=nested_struct_name, scheme=field)
                
                # Update v_type to the newly generated nested struct name
                v_type = nested_struct_name
            
            # Update the properties dictionary with type name and description
            properties[field_name] = {
                'type_name': v_type,
                'description': field.description  # type: ignore
            }

        code += "\n"
        code += self.struct_template.render(
            struct_name=struct_name,
            properties= properties # type: ignore
        )
        code += "\n"

        return code

    def _generate_structs(self) -> str:
        """
        Generate V structs from OpenAPI components with support for nested objects and arrays.
        """
        if not self.python_code.components:
            raise ValueError("No components found in spec")

        if not self.python_code.components.schemas:
            raise ValueError("No schemas found in components")

        code = ""

        for struct_name, schema in self.python_code.components.schemas.items():
            code += self._generate_struct(struct_name=struct_name, scheme=schema)

        return code 

        # structs_code = []
        # for schema_name, schema in self.python_code.components.schemas.items():
        #     fields = []
        #     for field_name, field in schema.properties.items():  # type: ignore
        #         if field.type == "object": # type: ignore
        #             # Generate a nested struct
        #             parts = field_name.split("_")
        #             nested_struct_name = ""
        #             for part in parts:
        #                 nested_struct_name += part.capitalize()
        #             nested_struct = self._generate_struct_from_object(nested_struct_name, field) # type: ignore
        #             structs_code.append(nested_struct)
        #             fields.append(f"\t{field_name} {nested_struct_name}")
        #             print(f"Generated struct for {nested_struct_name}")
        #         elif field.type == "array": # type: ignore
        #             # Handle arrays with proper type conversion for items
        #             item_type = self._convert_type(field.items.type)  # type: ignore
        #             fields.append(f"\t{field_name} []{item_type}")
        #         else:
        #             # Convert JSON schema type to V type
        #             v_type = self._convert_type(field.type)  # type: ignore
        #             fields.append(f"\t{field_name} {v_type}")

        #     # Construct struct
        #     struct_code = f"pub struct {schema_name} {{\n" + "\n".join(fields) + "\n}"
        #     structs_code.append(struct_code)
        #     print(f"Generated struct for {schema_name}")

        # return "\n\n".join(structs_code)

    # def _generate_struct_from_object(self, struct_name: str, schema: dict) -> str:
    #     """
    #     Generate a nested struct from an object schema.
    #     """
    #     fields = []
    #     for field_name, field in schema.properties.items():  # type: ignore
    #         v_type = self._convert_type(field.type)  # type: ignore
    #         fields.append(f"\t{field_name} {v_type}")

    #     return f"struct {struct_name} {{\n" + "\n".join(fields) + "\n}"

    # def _generate_methods(self) -> str:
    #     """
    #     Generate V methods based on OpenAPI paths and operations.
    #     """
    #     if not self.python_code.paths:
    #         raise ValueError("No paths found in spec")

    #     methods_code = []
    #     for path, path_item in self.python_code.paths.items():
    #         # Explicitly check for HTTP method attributes in PathItem
    #         for http_method in ["get", "post", "put", "delete", "patch", "options", "head"]:
    #             operation = getattr(path_item, http_method, None)
    #             if operation:
    #                 # Generate method name and parameters
    #                 method_name = self._generate_method_name(http_method, path)
    #                 parameters = self._generate_method_parameters(operation.parameters)
    #                 request_body = self._generate_request_body(operation.request_body)
    #                 response_type = self._generate_response_type(operation.responses)

    #                 # Combine method arguments
    #                 method_arguments = parameters
    #                 if request_body:
    #                     method_arguments += f", {request_body}" if parameters else request_body

    #                 # Generate the method code
    #                 method_code = f"fn {method_name}({method_arguments}) {response_type} {{\n"
    #                 method_code += f"\t// TODO: Implement the {http_method.upper()} request to {path}\n"
    #                 method_code += "\t// Use the generated structs for request/response bodies\n"
    #                 method_code += "}\n"
    #                 methods_code.append(method_code)

    #                 print(f"Generated method for {http_method.upper()} {path}")

    #     return "\n\n".join(methods_code)

    # def _generate_method_name(self, http_method: str, path: str) -> str:
    #     """
    #     Generate a method name from the HTTP method and path.
    #     """
    #     # Remove leading/trailing slashes and replace `/` with `_`
    #     sanitized_path = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
    #     return f"{http_method.lower()}_{sanitized_path}"

    # def _generate_method_parameters(self, parameters) -> str:
    #     if not parameters:
    #         return ""

    #     param_list = []
    #     for param in parameters:
    #         param_name = param.name
    #         param_schema = getattr(param, "schema", None)
    #         print('param_name: ', param_name)
    #         print('param_schema: ', param_schema)
    #         # if param_schema and param_schema.type:
    #         #     param_type = self._convert_type(param_schema.type)
    #         #     param_list.append(f"{param_name} {param_type}")

    #     return ", ".join(param_list)


    # def _generate_request_body(self, request_body) -> str:
    #     """
    #     Generate a function parameter for the request body if present.
    #     """
    #     if not request_body or not request_body.content:
    #         return ""

    #     # Assume application/json content type
    #     json_schema = request_body.content.get("application/json")
    #     if not json_schema or not json_schema.schema:
    #         return ""

    #     print('body_type: ', json_schema)
    #     # body_type = json_schema.schema.ref.split("/")[-1]  # Extract the schema name
    #     return f"body {json_schema}"

    # def _generate_response_type(self, responses) -> str:
    #     """
    #     Determine the return type of the method based on responses.
    #     """
    #     if not responses:
    #         return "void"

    #     for status_code, response in responses.items():
    #         if response.content and "application/json" in response.content:
    #             json_schema = response.content["application/json"].schema
    #             print('json_schema: ', json_schema)
    #             # if json_schema and json_schema.ref:
    #             #     return json_schema.ref.split("/")[-1]  # Extract schema name

    #     return "void"

    def _convert_type(self, json_type: str) -> str:
        """
        Map JSON schema types to Vlang types.
        """
        type_mapping = {
            "string": "string",
            "integer": "int",
            "number": "f64",
            "boolean": "bool",
            "array": "[]",
        }
        return type_mapping.get(json_type, "string")  # Default to `string`


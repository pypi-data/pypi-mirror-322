from inspect import isclass
from typing import Any, Dict, List

from pydantic import BaseModel


def get_pydantic_type(schema: Dict[str, Any]) -> str:
    """
    Convert OpenRPC schema types to Pydantic types.

    Args:
        schema: OpenRPC schema dictionary

    Returns:
        String representation of the Pydantic type
    """
    if "type" in schema:
        if schema["type"] == "string":
            if "format" in schema and schema["format"] == "email":
                return "Email"
            return "str"
        elif schema["type"] == "integer":
            return "int"
        elif schema["type"] == "array":
            items_type = get_pydantic_type(schema["items"])
            return f"List[{items_type}]"
        elif schema["type"] == "object":
            return "dict"
        elif schema["type"] == "boolean":
            return "bool"
        elif schema["type"] == "null":
            return "None"
    elif "$ref" in schema:
        ref_name = schema["$ref"].split("/")[-1]
        return ref_name
    elif "anyOf" in schema:
        types = [get_pydantic_type(sub_schema) for sub_schema in schema["anyOf"]]
        if "None" in types:
            # Remove 'None' from the types list
            types = [t for t in types if t != "None"]
            if len(types) == 1:
                return f"Optional[{types[0]}]"
            else:
                return f"Optional[Union[{', '.join(types)}]]"
        else:
            return f"Union[{', '.join(types)}]"

    return "Any"


def get_return_type(method_result: Dict[str, Any]) -> str:
    """
    Get the return type from a method result schema.

    Args:
        method_result: Method result dictionary containing schema or $ref

    Returns:
        String representation of the return type
    """
    if "schema" in method_result:
        schema = method_result["schema"]
        if "type" in schema:
            return get_pydantic_type(schema)
        elif "$ref" in schema:
            ref_name = schema["$ref"].split("/")[-1]
            return ref_name
        elif "anyOf" in schema:
            schema_list = schema["anyOf"]
            if isinstance(schema_list, list):
                return " | ".join(get_pydantic_type(sub_schema) for sub_schema in schema_list)
            return "Any"
    elif "$ref" in method_result:  # Handle $ref at the top level
        ref_path = method_result["$ref"]
        if isinstance(ref_path, str):
            return ref_path.split("/")[-1]
    return ""


def topological_sort(schema_dict: Dict[str, Any]) -> List[str]:
    visited = set()
    stack = []
    sorted_classes = []

    def dfs(class_name: str) -> None:
        visited.add(class_name)
        if class_name in schema_dict:
            for prop in schema_dict[class_name].get("properties", {}).values():
                if "$ref" in prop:
                    ref_name = prop["$ref"].split("/")[-1]
                    if ref_name not in visited:
                        dfs(ref_name)
        stack.append(class_name)

    for class_name in schema_dict:
        if class_name not in visited:
            dfs(class_name)

    while stack:
        sorted_classes.append(stack.pop())

    return sorted_classes


def create_example_object(cls: type[BaseModel]) -> BaseModel:
    """
    Create an example object from a Pydantic model class using field examples.

    Args:
        cls: A Pydantic BaseModel class

    Returns:
        An instance of the provided model class with example data

    Raises:
        ValueError: If cls is not a valid Pydantic BaseModel class
    """
    if not isclass(cls) or not issubclass(cls, BaseModel):
        raise ValueError(f"{cls} is not a valid pydantic BaseModel class.")

    example_data = {}

    for field_name, field_info in cls.model_fields.items():
        examples = field_info.examples
        if examples:
            example_data[field_name] = examples[0]

    return cls(**example_data)

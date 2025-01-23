import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader

from ....openrpc.tools import get_pydantic_type, get_return_type, topological_sort

script_dir = os.path.dirname(os.path.abspath(__file__))


def generate_models(openrpc_spec: dict) -> str:
    schema_dict = openrpc_spec["components"]["schemas"]
    sorted_classes = topological_sort(schema_dict)

    env = Environment(loader=FileSystemLoader(script_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("templates/mdbook/structs.jinja")
    model_code = template.render(
        sorted_classes=sorted_classes,
        schema_dict=schema_dict,
        get_pydantic_type=get_pydantic_type,
    )

    return model_code


def generate_model(model_name: str, schema: dict) -> str:
    env = Environment(loader=FileSystemLoader(script_dir))
    template = env.get_template("templates/vlang/struct.jinja")
    model_code = template.render(model_name=model_name, schema=schema, get_pydantic_type=get_pydantic_type)

    return model_code


def generate_api_methods(openrpc_spec: dict) -> str:
    env = Environment(loader=FileSystemLoader(script_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("templates/mdbook/methods.jinja")

    code = template.render(
        spec=openrpc_spec,
        methods=openrpc_spec.get("methods", []),
        get_return_type=get_return_type,
        get_pydantic_type=get_pydantic_type,
    )

    return code


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate API code from OpenRPC specification")
    parser.add_argument(
        "-s",
        "--spec",
        help="Path to the specs (expressed in our own V format)",
        default="~/code/git.ourworld.tf/projectmycelium/hero_server/generatorexamples/example1/specs",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="/tmp/generator/mdbook",
        help="Output file path (default: /tmp/generator/mdbook)",
    )
    args = parser.parse_args()

    spec_file = os.path.expanduser(args.spec)
    output_dir = os.path.expanduser(args.output)

    if not os.path.isfile(spec_file):
        print(f"Error: OpenRPC specification file '{spec_file}' does not exist.")
        return

    with open(spec_file) as file:
        openrpc_spec = json.load(file)

    code_models = generate_models(openrpc_spec)
    code_methods = generate_api_methods(openrpc_spec)

    os.makedirs(os.path.dirname(output_dir), exist_ok=True)

    # Write the generated code to a file
    with open(f"{output_dir}/models.md", "w") as file:
        file.write(code_models)
    with open(f"{output_dir}/methods.md", "w") as file:
        file.write(code_methods)

    print(f"Generated API code has been written to {output_dir}")


if __name__ == "__main__":
    main()

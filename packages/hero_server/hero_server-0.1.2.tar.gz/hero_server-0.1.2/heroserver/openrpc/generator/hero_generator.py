import argparse
from pathlib import Path

from heroserver.openrpc.generator.rest_server.python.rest_server_generator import (
    RestServerGenerator,
)
from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec
from heroserver.openrpc.parser.parser import parser


def do(specs_dir: Path, output: Path):
    for item in specs_dir.iterdir():
        if not item.is_dir():
            continue

        actor_name = item.name
        actor_output_path = output.joinpath(actor_name)
        actor_output_path.mkdir(parents=True, exist_ok=True)

        print(f"item: {item.as_posix()}")
        # if item.as_posix() == "generatorexamples/example1/specs/storymanager":
        #     continue
        data = parser(path=item.as_posix())
        # print(f"data: {data}")
        spec_object = OpenRPCSpec.load(data)
        server_generator = RestServerGenerator(spec_object, actor_output_path)
        server_generator.generate()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Hero server and client generator tool.")
    arg_parser.add_argument(
        "--specs",
        type=str,
        required=True,
        help="specs directory",
    )
    arg_parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="output directory",
    )

    args = arg_parser.parse_args()
    do(Path(args.specs), Path(args.output))

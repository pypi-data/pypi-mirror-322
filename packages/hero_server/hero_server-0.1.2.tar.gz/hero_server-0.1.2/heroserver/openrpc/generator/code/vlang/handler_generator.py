import os
from pathlib import Path
from typing import Dict, Union

from jinja2 import Environment, FileSystemLoader

from heroserver.openrpc.generator.model_generator import ModelGenerator
from heroserver.openrpc.generator.vlang.vlang_code_generator import VlangGenerator
from heroserver.openrpc.model.common import ContentDescriptorObject, ReferenceObject
from heroserver.openrpc.model.methods import MethodObject
from heroserver.openrpc.model.openrpc_spec import OpenRPCSpec

script_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(script_dir))


def get_actor_executor_name(actor: str) -> str:
    return f"{''.join([part.title() for part in actor.split('_')])}Executor"


class ActorGenerator:
    def __init__(self, actor: str, spec: OpenRPCSpec, dir: Path) -> None:
        self.spec = spec
        self.actor = actor
        self.dir = dir
        self.model_generator = ModelGenerator(spec, VlangGenerator())
        self.executor_template = env.get_template("templates/executor.jinja")
        self.pre_template = env.get_template("templates/pre.jinja")
        self.internal_crud_methods_template = env.get_template("templates/internal_crud_methods.jinja")
        self.internal_actor_method_template = env.get_template("templates/internal_actor_method.jinja")

    def generate(self):
        self.generate_models()
        self.generate_crud()
        self.generate_internal_actor_methods()
        self.generate_executor()

    def generate_models(self):
        pre = self.pre_template.render(module_name="myhandler", imports=[])
        code = self.model_generator.generate_models()
        path = self.dir.joinpath(f"{self.actor}_models.v")

        with open(path, "w") as file:
            file.write(f"{pre}\n\n{code}\n")

    def generate_crud(self):
        imports = self.pre_template.render(
            module_name="myhandler",
            imports=["json", "freeflowuniverse.crystallib.baobab.backend"],
        )
        methods = ""
        for path_str in self.model_generator.spec.get_root_objects().keys():
            object = self.model_generator.processed_objects[path_str]
            if object["code"] == "":
                continue

            type_name = object["name"]
            variable_name = type_name.lower()
            methods += (
                self.internal_crud_methods_template.render(
                    variable_name=variable_name,
                    type_name=type_name,
                    actor_executor_name=get_actor_executor_name(self.actor),
                )
                + "\n\n"
            )

        path = self.dir.joinpath(f"{self.actor}_crud.v")
        with open(path, "w") as file:
            file.write(f"{imports}\n\n{methods}")

    def generate_internal_actor_methods(self):
        pre = self.pre_template.render(module_name="myhandler", imports=[])
        for method in self.spec.methods:
            function_name = method.name.lower().replace(".", "_") + "_internal"
            file_path = self.dir.joinpath(f"{self.actor}_{function_name}.v")
            if file_path.exists():
                continue

            if any(method.name.endswith(end) for end in ["get", "set", "delete"]):
                continue

            params: Dict[str, str] = {}
            for param in method.params:
                params[param.name] = self.model_generator.jsonschema_to_type(["methods", method.name, "params", param.name], param.schema)

            return_type = self.get_method_return_type(method)
            method_params = ", ".join([f"{param.name} {self.get_param_type(method.name, param)}" for param in method.params])

            code = self.internal_actor_method_template.render(
                function_name=function_name,
                method_params=method_params,
                return_type=return_type,
                actor_executor_name=get_actor_executor_name(self.actor),
            )

            with open(file_path, "w") as file:
                file.write(f"{pre}\n\n{code}")

    def generate_executor(self):
        pre = self.pre_template.render(
            module_name="myhandler",
            imports=[
                "x.json2",
                "json",
                "freeflowuniverse.crystallib.clients.redisclient",
                "freeflowuniverse.crystallib.baobab.backend",
                "freeflowuniverse.crystallib.rpc.jsonrpc",
            ],
        )

        code = self.executor_template.render(
            generator=self,
            actor_executor_name=get_actor_executor_name(self.actor),
            methods=self.spec.methods,
        )

        path = self.dir.joinpath(f"{self.actor}_executor.v")
        with open(path, "w") as file:
            file.write(f"{pre}\n\n{code}")

    def get_param_type(
        self,
        method_name: str,
        param: Union[ContentDescriptorObject, ReferenceObject],
    ) -> str:
        type_name = self.model_generator.jsonschema_to_type(["methods", method_name, "params", param.name], param.schema)
        return type_name

    def get_method_return_type(self, method: MethodObject) -> str:
        if not method.result:
            return ""

        path = ["methods", method.name, "result"]
        schema = method.result
        if isinstance(method.result, ContentDescriptorObject):
            schema = method.result.schema

        return self.model_generator.jsonschema_to_type(path, schema)

    def is_primitive(self, type_name: str) -> bool:
        return self.model_generator.lang_code_generator.is_primitive(type_name)

    def get_method_params_as_args(self, method: MethodObject) -> str:
        return ", ".join([param.name for param in method.params])


class Generator:
    def generate_handler(self, specs_dir: Path, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)

        handler_template = env.get_template("templates/handler.jinja")
        handler_test_template = env.get_template("templates/handler_test.jinja")
        pre_template = env.get_template("templates/pre.jinja")
        actors = []
        method_names = []

        pre = pre_template.render(
            module_name="myhandler",
            imports=[
                "freeflowuniverse.crystallib.clients.redisclient",
                "freeflowuniverse.crystallib.baobab.backend",
                "freeflowuniverse.crystallib.rpc.jsonrpc",
            ],
        )
        code = ""
        for item in specs_dir.iterdir():
            if not item.is_dir():
                continue

            actors.append(item.name)

            data = parser(path=item.as_posix())
            openrpc_spec = OpenRPCSpec.load(data)
            actor_generator = ActorGenerator(item.name, openrpc_spec, output_dir)
            actor_generator.generate()

            for method in openrpc_spec.methods:
                method_names.append(f"{item.name}.{method.name}")

        code = handler_template.render(actors=actors, get_actor_executor_name=get_actor_executor_name)

        handler_path = output_dir.joinpath("handler.v")
        with open(handler_path, "w") as file:
            file.write(f"{pre}\n\n{code}")

        handler_test_path = output_dir.joinpath("handler_test.v")
        with open(handler_test_path, "w") as file:
            file.write(handler_test_template.render(method_names=method_names))


if __name__ == "__main__":
    from heroserver.openrpc.parser.parser import parser

    generator = Generator()
    path = "~/code/git.ourworld.tf/projectmycelium/hero_server/generatorexamples/example1/specs"
    generator.generate_handler(Path(path), Path("/tmp/myhandler"))
    # vlang_code_generator = VlangGenerator()
    # generator = ClientGenerator(
    #     spec_object,
    #     vlang_code_generator,
    #     "/tmp/v_client_new.v",
    # )

    # generator.generate_client()

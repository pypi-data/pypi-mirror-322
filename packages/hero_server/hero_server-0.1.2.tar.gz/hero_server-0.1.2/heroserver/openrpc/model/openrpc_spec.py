from typing import Any, Dict, List, Optional, Union

from heroserver.openrpc.model.common import (
    ContentDescriptorObject,
    ExternalDocumentationObject,
    ReferenceObject,
    SchemaObject,
)
from heroserver.openrpc.model.components import ComponentsObject
from heroserver.openrpc.model.info import InfoObject
from heroserver.openrpc.model.methods import MethodObject
from heroserver.openrpc.model.server import ServerObject

ROOT_OBJ_DEF = "!!define.root_object"


class OpenRPCSpec:
    def __init__(
        self,
        openrpc: str,
        info: InfoObject,
        methods: List[MethodObject],
        servers: Optional[List[ServerObject]] = None,
        components: Optional[ComponentsObject] = None,
        externalDocs: Optional[ExternalDocumentationObject] = None,
        spec_extensions: Optional[Dict[str, Any]] = None,
    ):
        self.openrpc = openrpc
        self.info = info
        self.servers = servers
        self.methods = methods
        self.components = components
        self.externalDocs = externalDocs
        self.spec_extensions = spec_extensions

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "OpenRPCSpec":
        return cls(
            openrpc=data["openrpc"],
            info=InfoObject.load(data["info"]),
            servers=([ServerObject.load(item) for item in data.get("servers", [])] if "servers" in data else None),
            methods=[MethodObject.load(item) for item in data["methods"]],
            components=(ComponentsObject.load(data["components"]) if "components" in data else None),
            externalDocs=(ExternalDocumentationObject.load(data["externalDocs"]) if "externalDocs" in data else None),
            spec_extensions=data.get("spec_extensions"),
        )

    def ref_to_schema(self, ref: str) -> Union[SchemaObject, ContentDescriptorObject]:
        if not ref.startswith("#/"):
            raise Exception(f"invalid ref: {ref}")

        l = ref.split("/")[1:]
        obj = self
        for item in l:
            # TODO: find root cause of RO_
            if item.startswith("RO_"):
                item = item[3:]

            if isinstance(obj, Dict):
                print("obj contents: ", obj)
                print("Trying to access key: ", item)
                obj = obj[item]
            else:
                obj = obj.__dict__[item]

        if not isinstance(obj, SchemaObject) and not isinstance(obj, ContentDescriptorObject):
            raise Exception(f"ref to unsupported type: {ref}")

        return obj

    def get_root_objects(self) -> Dict[str, SchemaObject]:
        if not self.components:
            return {}

        objs: Dict[str, SchemaObject] = {}
        base_ref = ["components", "schemas"]
        for name, scheme in self.components.schemas.items():
            if scheme.xtags and "rootobject" in scheme.xtags:
                objs["/".join(base_ref + [name.lower()])] = scheme

        return objs

    def set_root_objects(self, refs: List[str]):
        for ref in refs:
            obj = self.ref_to_schema(ref)
            if isinstance(obj, ContentDescriptorObject):
                obj = obj.schema
                if isinstance(obj, ReferenceObject):
                    self.set_root_objects([obj.ref])
                    continue

            if not obj.description:
                obj.description = ROOT_OBJ_DEF
            else:
                obj.description += f";{ROOT_OBJ_DEF}"


# Note that classes that refer to themselves or each other are handled using string literals in annotations to avoid forward reference issues. Python 3.7+ supports this feature with the use of 'from __future__ import annotations'.

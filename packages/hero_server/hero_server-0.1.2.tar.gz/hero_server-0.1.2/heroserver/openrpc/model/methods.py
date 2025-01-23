from typing import Any, Dict, List, Optional, Union

from heroserver.openrpc.model.common import (
    ContentDescriptorObject,
    ErrorObject,
    ExamplePairingObject,
    ExternalDocumentationObject,
    ReferenceObject,
    TagObject,
)
from heroserver.openrpc.model.server import LinkObject, ServerObject


class MethodObject:
    def __init__(
        self,
        name: str,
        params: List[Union[ContentDescriptorObject, ReferenceObject]],
        result: Union[ContentDescriptorObject, ReferenceObject, None],
        tags: Optional[List[Union[TagObject, ReferenceObject]]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        externalDocs: Optional[ExternalDocumentationObject] = None,
        deprecated: Optional[bool] = None,
        servers: Optional[List[ServerObject]] = None,
        errors: Optional[List[Union[ErrorObject, ReferenceObject]]] = None,
        links: Optional[List[Union[LinkObject, ReferenceObject]]] = None,
        paramStructure: Optional[str] = None,
        examples: Optional[List[ExamplePairingObject]] = None,
    ):
        self.name = name
        self.tags = tags
        self.summary = summary
        self.description = description
        self.externalDocs = externalDocs
        self.params = params
        self.result = result
        self.deprecated = deprecated
        self.servers = servers
        self.errors = errors
        self.links = links
        self.paramStructure = paramStructure
        self.examples = examples

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "MethodObject":
        return cls(
            name=data["name"],
            tags=(
                [
                    (TagObject.load(item) if isinstance(item, dict) and "name" in item else ReferenceObject.load(item))
                    for item in data.get("tags", [])
                ]
                if "tags" in data
                else None
            ),
            summary=data.get("summary"),
            description=data.get("description"),
            externalDocs=(ExternalDocumentationObject.load(data["externalDocs"]) if "externalDocs" in data else None),
            params=[
                (ContentDescriptorObject.load(item) if isinstance(item, dict) and "name" in item else ReferenceObject.load(item))
                for item in data["params"]
            ],
            result=(
                ContentDescriptorObject.load(data["result"])
                if isinstance(data["result"], dict) and "name" in data["result"]
                else ReferenceObject.load(data["result"])
                if "result" in data
                else None
            ),
            deprecated=data.get("deprecated"),
            servers=([ServerObject.load(item) for item in data.get("servers", [])] if "servers" in data else None),
            errors=(
                [
                    (ErrorObject.load(item) if isinstance(item, dict) and "code" in item else ReferenceObject.load(item))
                    for item in data.get("errors", [])
                ]
                if "errors" in data
                else None
            ),
            links=(
                [
                    (LinkObject.load(item) if isinstance(item, dict) and "name" in item else ReferenceObject.load(item))
                    for item in data.get("links", [])
                ]
                if "links" in data
                else None
            ),
            paramStructure=data.get("paramStructure"),
            examples=([ExamplePairingObject.load(item) for item in data.get("examples", [])] if "examples" in data else None),
        )

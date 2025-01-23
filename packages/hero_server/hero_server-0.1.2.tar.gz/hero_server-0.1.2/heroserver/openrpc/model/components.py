from typing import Any, Dict, Union

from heroserver.openrpc.model.common import (
    ContentDescriptorObject,
    ErrorObject,
    ExampleObject,
    ExamplePairingObject,
    ReferenceObject,
    SchemaObject,
    TagObject,
)
from heroserver.openrpc.model.server import LinkObject


class ComponentsObject:
    def __init__(
        self,
        contentDescriptors: Dict[str, ContentDescriptorObject],
        schemas: Dict[str, Union[SchemaObject, ReferenceObject]],
        examples: Dict[str, ExampleObject],
        links: Dict[str, LinkObject],
        errors: Dict[str, ErrorObject],
        examplePairingObjects: Dict[str, ExamplePairingObject],
        tags: Dict[str, TagObject],
    ):
        self.contentDescriptors = contentDescriptors
        self.schemas = schemas
        self.examples = examples
        self.links = links
        self.errors = errors
        self.examplePairingObjects = examplePairingObjects
        self.tags = tags

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ComponentsObject":
        return cls(
            contentDescriptors={k: ContentDescriptorObject.load(v) for k, v in data.get("contentDescriptors", {}).items()},
            schemas={k: ReferenceObject.load(v) if "$ref" in v else SchemaObject.load(v) for k, v in data.get("schemas", {}).items()},
            examples={k: ExampleObject.load(v) for k, v in data.get("examples", {}).items()},
            links={k: LinkObject.load(v) for k, v in data.get("links", {}).items()},
            errors={k: ErrorObject.load(v) for k, v in data.get("errors", {}).items()},
            examplePairingObjects={k: ExamplePairingObject.load(v) for k, v in data.get("examplePairingObjects", {}).items()},
            tags={k: TagObject.load(v) for k, v in data.get("tags", {}).items()},
        )

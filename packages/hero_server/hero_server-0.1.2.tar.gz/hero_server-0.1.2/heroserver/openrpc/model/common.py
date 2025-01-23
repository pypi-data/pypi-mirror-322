from typing import Any, Dict, List, Optional, Union


class ReferenceObject:
    def __init__(self, ref: str = ""):
        self.ref = ref

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ReferenceObject":
        return cls(ref=data.get("$ref", ""))


class SchemaObject:
    def __init__(
        self,
        title: Optional[str] = None,
        multipleOf: Optional[float] = None,
        maximum: Optional[float] = None,
        exclusiveMaximum: Optional[bool] = None,
        minimum: Optional[float] = None,
        exclusiveMinimum: Optional[bool] = None,
        maxLength: Optional[int] = None,
        minLength: Optional[int] = None,
        pattern: Optional[str] = None,
        maxItems: Optional[int] = None,
        minItems: Optional[int] = None,
        uniqueItems: Optional[bool] = None,
        maxProperties: Optional[int] = None,
        minProperties: Optional[int] = None,
        required: Optional[List[str]] = None,
        enum: Optional[List[Any]] = None,
        type: Optional[str] = None,
        allOf: Optional[List[Union["SchemaObject", ReferenceObject]]] = None,
        oneOf: Optional[List[Union["SchemaObject", ReferenceObject]]] = None,
        anyOf: Optional[List[Union["SchemaObject", ReferenceObject]]] = None,
        not_: Optional[Union["SchemaObject", ReferenceObject]] = None,
        items: Optional[
            Union[
                "SchemaObject",
                ReferenceObject,
                List[Union["SchemaObject", ReferenceObject]],
            ]
        ] = None,
        properties: Optional[Dict[str, Union["SchemaObject", ReferenceObject]]] = None,
        additionalProperties: Optional[Union[bool, "SchemaObject"]] = None,
        description: Optional[str] = None,
        format: Optional[str] = None,
        default: Optional[Any] = None,
        xtags: Optional[List[str]] = None,
        example: Optional[str] = None,
    ):
        self.title = title
        self.multipleOf = multipleOf
        self.maximum = maximum
        self.exclusiveMaximum = exclusiveMaximum
        self.minimum = minimum
        self.exclusiveMinimum = exclusiveMinimum
        self.maxLength = maxLength
        self.minLength = minLength
        self.pattern = pattern
        self.maxItems = maxItems
        self.minItems = minItems
        self.uniqueItems = uniqueItems
        self.maxProperties = maxProperties
        self.minProperties = minProperties
        self.required = required
        self.enum = enum
        self.type = type
        self.allOf = allOf
        self.oneOf = oneOf
        self.anyOf = anyOf
        self.not_ = not_
        self.items = items
        self.properties = properties
        self.additionalProperties = additionalProperties
        self.description = description
        self.format = format
        self.default = default
        self.xtags = xtags
        self.example = example

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "SchemaObject":
        return cls(
            title=data.get("title"),
            multipleOf=data.get("multipleOf"),
            maximum=data.get("maximum"),
            exclusiveMaximum=data.get("exclusiveMaximum"),
            minimum=data.get("minimum"),
            exclusiveMinimum=data.get("exclusiveMinimum"),
            maxLength=data.get("maxLength"),
            minLength=data.get("minLength"),
            pattern=data.get("pattern"),
            maxItems=data.get("maxItems"),
            minItems=data.get("minItems"),
            uniqueItems=data.get("uniqueItems"),
            maxProperties=data.get("maxProperties"),
            minProperties=data.get("minProperties"),
            required=data.get("required"),
            enum=data.get("enum"),
            type=data.get("type"),
            allOf=(
                [
                    (
                        ReferenceObject.load(item)
                        if "$ref" in item
                        else SchemaObject.load(item)
                    )
                    for item in data.get("allOf", [])
                ]
                if "allOf" in data
                else None
            ),
            oneOf=(
                [
                    (
                        ReferenceObject.load(item)
                        if "$ref" in item
                        else SchemaObject.load(item)
                    )
                    for item in data.get("oneOf", [])
                ]
                if "oneOf" in data
                else None
            ),
            anyOf=(
                [
                    (
                        ReferenceObject.load(item)
                        if "$ref" in item
                        else SchemaObject.load(item)
                    )
                    for item in data.get("anyOf", [])
                ]
                if "anyOf" in data
                else None
            ),
            not_=(
                (
                    ReferenceObject.load(data)
                    if "$ref" in data
                    else SchemaObject.load(data)
                )
                if "not" in data
                else None
            ),
            items=(
                (
                    ReferenceObject.load(data["items"])
                    if "$ref" in data["items"]
                    else SchemaObject.load(data["items"])
                )
                if isinstance(data.get("items"), dict)
                else (
                    [
                        (
                            ReferenceObject.load(item)
                            if "$ref" in item
                            else SchemaObject.load(item)
                        )
                        for item in data.get("items", [])
                    ]
                    if "items" in data
                    else None
                )
            ),
            properties=(
                {
                    k: (
                        ReferenceObject.load(v) if "$ref" in v else SchemaObject.load(v)
                    )
                    for k, v in data.get("properties", {}).items()
                }
                if "properties" in data
                else None
            ),
            additionalProperties=(
                SchemaObject.load(data["additionalProperties"])
                if isinstance(data.get("additionalProperties"), dict)
                else data.get("additionalProperties")
            ),
            description=data.get("description"),
            format=data.get("format"),
            default=data.get("default"),
            xtags=data.get("x-tags"),
            example=data.get("example"),
        )


class ContentDescriptorObject:
    def __init__(
        self,
        name: str,
        schema: Union[SchemaObject, ReferenceObject],
        summary: Optional[str] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        deprecated: Optional[bool] = None,
    ):
        self.name = name
        self.summary = summary
        self.description = description
        self.required = required
        self.schema = schema
        self.deprecated = deprecated

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ContentDescriptorObject":
        return cls(
            name=data["name"],
            summary=data.get("summary"),
            description=data.get("description"),
            required=data.get("required"),
            schema=(
                ReferenceObject.load(data["schema"])
                if "$ref" in data["schema"]
                else SchemaObject.load(data["schema"])
            ),
            deprecated=data.get("deprecated"),
        )


class ExternalDocumentationObject:
    def __init__(self, url: str, description: Optional[str] = None):
        self.description = description
        self.url = url

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ExternalDocumentationObject":
        return cls(description=data.get("description"), url=data["url"])


class ExampleObject:
    def __init__(
        self,
        name: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        value: Optional[Any] = None,
        externalValue: Optional[str] = None,
    ):
        self.name = name
        self.summary = summary
        self.description = description
        self.value = value
        self.externalValue = externalValue

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ExampleObject":
        return cls(
            name=data["name"],
            summary=data.get("summary"),
            description=data.get("description"),
            value=data.get("value"),
            externalValue=data.get("externalValue"),
        )


class ErrorObject:
    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        self.code = code
        self.message = message
        self.data = data

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ErrorObject":
        return cls(code=data["code"], message=data["message"], data=data.get("data"))


class ExamplePairingObject:
    def __init__(
        self,
        name: str,
        result: Union[ExampleObject, ReferenceObject],
        params: List[ExampleObject],
        description: Optional[str] = None,
        summary: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.summary = summary
        self.params = params
        self.result = result

    def get_x() -> Union[str, int]:
        a = [1, 2, 3]
        b = ["a", "b", "c"]
        z = Union()

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ExamplePairingObject":
        return cls(
            name=data["name"],
            description=data.get("description"),
            summary=data.get("summary"),
            params=[ExampleObject.load(item) for item in data["params"]],
            result=(
                ExampleObject.load(data["result"])
                if isinstance(data["result"], dict) and "value" in data["result"]
                else ReferenceObject.load(data["result"])
            ),
        )


class TagObject:
    def __init__(
        self,
        name: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        externalDocs: Optional[ExternalDocumentationObject] = None,
    ):
        self.name = name
        self.summary = summary
        self.description = description
        self.externalDocs = externalDocs

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "TagObject":
        return cls(
            name=data["name"],
            summary=data.get("summary"),
            description=data.get("description"),
            externalDocs=(
                ExternalDocumentationObject.load(data["externalDocs"])
                if "externalDocs" in data
                else None
            ),
        )

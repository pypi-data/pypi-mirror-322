from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from urllib.parse import ParseResult

from heroserver.openrpc.model.common import (
    ReferenceObject,
    SchemaObject,
)
from heroserver.openrpc.model.methods import MethodObject


class PropertyInfo:
    def __init__(
        self,
        name: str,
        type_name: str,
        description: Optional[str] = None,
        example: Optional[str] = None,
    ) -> None:
        self.name = name
        self.type_name = type_name
        self.description = description
        self.example = example


class LangCodeGenerator(ABC):
    @abstractmethod
    def generate_imports(self) -> str:
        pass

    @abstractmethod
    def generate_object(
        self,
        type_name: str,
        properties: Dict[str, PropertyInfo],
    ):
        pass

    @abstractmethod
    def generate_method(
        self,
        method_spec: MethodObject,
        url: ParseResult,
        params: Dict[str, str],
        return_type: str,
    ) -> str:
        pass

    @abstractmethod
    def string_primitive(self) -> str:
        pass

    @abstractmethod
    def integer_primitive(self) -> str:
        pass

    @abstractmethod
    def number_primitive(self) -> str:
        pass

    @abstractmethod
    def null_primitive(self) -> str:
        pass

    @abstractmethod
    def bool_primitive(self) -> str:
        pass

    @abstractmethod
    def is_primitive(self, type_name: str) -> bool:
        pass

    @abstractmethod
    def generate_multitype(self, path: List[str], types: List[Union[SchemaObject, ReferenceObject]]) -> str:
        """handles `anyOf` and `oneOf` in a json schema"""
        pass

    @abstractmethod
    def array_of_type(self, type_name: str) -> str:
        pass

    @abstractmethod
    def encapsulate_types(self, path: List[str], types: List[Union[SchemaObject, ReferenceObject]]) -> str:
        """handles `allOf` in a json schema"""
        pass

    @abstractmethod
    def generate_enum(self, enum: List[Any], type_name: str) -> str:
        pass

    @abstractmethod
    def type_to_method_result(self, type_name: str) -> str:
        """
        convert type to method result
        - type_name can be empty
        """
        pass

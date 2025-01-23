from typing import Any, Dict, List, Optional, Union


class ServerVariableObject:
    def __init__(
        self,
        default: str,
        enum: Optional[List[str]] = None,
        description: Optional[str] = None,
    ):
        self.enum = enum
        self.default = default
        self.description = description

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ServerVariableObject":
        return cls(
            enum=data.get("enum"),
            default=data["default"],
            description=data.get("description"),
        )


class ServerObject:
    def __init__(
        self,
        name: str,
        url: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        variables: Optional[Dict[str, ServerVariableObject]] = None,
    ):
        self.name = name
        self.url = url
        self.summary = summary
        self.description = description
        self.variables = variables

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ServerObject":
        variables = (
            {
                k: ServerVariableObject.load(v)
                for k, v in data.get("variables", {}).items()
            }
            if "variables" in data
            else None
        )
        return cls(
            name=data["name"],
            url=data["url"],
            summary=data.get("summary"),
            description=data.get("description"),
            variables=variables,
        )


class LinkObject:
    def __init__(
        self,
        name: str,
        method: str,
        params: Dict[str, Any],
        description: Optional[str] = None,
        summary: Optional[str] = None,
        server: Optional[ServerObject] = None,
    ):
        self.name = name
        self.description = description
        self.summary = summary
        self.method = method
        self.params = params
        self.server = server

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "LinkObject":
        return cls(
            name=data["name"],
            description=data.get("description"),
            summary=data.get("summary"),
            method=data["method"],
            params=data["params"],
            server=ServerObject.load(data["server"]) if "server" in data else None,
        )

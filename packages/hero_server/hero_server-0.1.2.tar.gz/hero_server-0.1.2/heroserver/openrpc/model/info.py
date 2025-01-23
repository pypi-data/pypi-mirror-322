from typing import Any, Dict, Optional


class ContactObject:
    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        email: Optional[str] = None,
    ):
        self.name = name
        self.url = url
        self.email = email

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "ContactObject":
        return cls(name=data.get("name"), url=data.get("url"), email=data.get("email"))


class LicenseObject:
    def __init__(self, name: str, url: Optional[str] = None):
        self.name = name
        self.url = url

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "LicenseObject":
        return cls(name=data["name"], url=data.get("url"))


class InfoObject:
    def __init__(
        self,
        title: str,
        version: str,
        description: Optional[str] = None,
        termsOfService: Optional[str] = None,
        contact: Optional[ContactObject] = None,
        license: Optional[LicenseObject] = None,
    ):
        self.title = title
        self.description = description
        self.termsOfService = termsOfService
        self.contact = contact
        self.license = license
        self.version = version

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "InfoObject":
        return cls(
            title=data["title"],
            description=data.get("description"),
            termsOfService=data.get("termsOfService"),
            contact=ContactObject.load(data["contact"]) if "contact" in data else None,
            license=LicenseObject.load(data["license"]) if "license" in data else None,
            version=data["version"],
        )

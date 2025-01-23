from typing import Dict, Generic, List, TypeVar

from infoserver.db import DB
from infoserver.model import RightEnum

T = TypeVar('T')


class DBMemCat(Generic[T]):
    def __init__(self, parent_cat):
        self.parent_cat = parent_cat
        self.items: Dict[str, T] = {}

    def set(self, item: T) -> T:
        self.items[item.name] = item
        self.parent_cat.set(item)
        return item

    def get(self, name: str) -> T:
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'name' to be of type str, but got {type(name).__name__}"
            )
        item = self.items.get(name)
        if item is None:
            raise KeyError(f'Item with name {name} not found.')
        return item

    def list(self) -> List[str]:
        return list(self.items.keys())


class DBMem:
    def __init__(self, parent: DB, current_user_email: str):
        if not isinstance(parent, DB):
            raise TypeError(
                f"Expected 'parent' to be of type FileSystemDatabase, but got {type(parent).__name__}"
            )

        self.parent = parent
        self.acls = DBMemCat(parent.acl)
        self.users = DBMemCat(parent.user)
        self.groups = DBMemCat(parent.group)
        self.infos = DBMemCat(parent.info)
        self.load()
        self.current_user = self.users.get(current_user_email)

    def load(self):
        self.acls.items = {
            acl_name: self.parent.acl.get(acl_name)
            for acl_name in self.parent.acl.list()
        }
        self.users.items = {
            user_email: self.parent.user.get(user_email)
            for user_email in self.parent.user.list()
        }
        self.groups.items = {
            group_name: self.parent.group.get(group_name)
            for group_name in self.parent.group.list()
        }
        self.infos.items = {
            info_name: self.parent.info.get(info_name)
            for info_name in self.parent.info.list()
        }

    def info_acl(self, info_name: str) -> RightEnum:
        highest = 0  # 0 is the lowest right, BLOCK
        info_mem = self.infos.get(info_name)
        for acl_name in info_mem.acl:
            acl = self.acls.get(acl_name)
            for entry in acl.entries:
                if highest == 3:
                    return RightEnum.admin
                if entry.user == self.current_user.email:
                    highest = max(highest, entry.right.level())
                if entry.group:
                    for userfound in self.group_get_users(entry.group):
                        if userfound == self.current_user.email:
                            highest = max(highest, entry.right.level())
        return RightEnum(highest)

    def info_acl_check(self, info_name: str, rightneeded: RightEnum) -> bool:
        highest_right = self.info_acl(info_name)
        return highest_right.level() >= rightneeded.level()

    def group_get_users(self, groupname: str) -> List[str]:
        group = self.groups.get(groupname)
        resolved_users = set(group.users)
        for group_name in group.groups:
            group = self.groups.get(group_name)
            resolved_users.update(self.group_get_users(group.name))
        return list(resolved_users)

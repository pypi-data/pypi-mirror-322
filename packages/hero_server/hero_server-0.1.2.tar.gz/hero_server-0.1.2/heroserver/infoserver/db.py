import os
import shutil
from pathlib import Path
from typing import Generic, List, Type, TypeVar

import toml
from infoserver.model import ACL, Group, InfoPointer, User
from infoserver.texttools import name_fix

T = TypeVar('T')


class ObjNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DBCat(Generic[T]):
    def __init__(self, db: 'DB', dir_name: str, model: Type[T]):
        self.db = db
        self.dir = db.base_dir / dir_name
        self.model = model
        self.dir.mkdir(parents=True, exist_ok=True)
        if self.db.debug:
            print(f'Initialized DBCat with base directory: {self.dir}')

    def exists(self, name: str) -> bool:
        name = name_fix(name)
        path = self.dir / f'{name}.toml'
        exists = path.exists()
        if self.db.debug:
            print(f'Checking existence of {path}: {exists}')
        return exists

    def identifier_get(self, obj: T) -> str:
        if isinstance(obj, User):
            identifier = name_fix(obj.email)
        elif not hasattr(obj, 'name'):
            raise AttributeError(
                f"Object of type {self.model.__name__} must have a 'name' attribute"
            )
        else:
            identifier = name_fix(obj.name)
        if self.db.debug:
            print(f'Generated identifier for {obj}: {identifier}')
        return identifier

    def set(self, obj: T) -> T:
        if not isinstance(obj, self.model):
            raise TypeError(
                f'Expected object of type {self.model.__name__}, got {type(obj).__name__}'
            )
        identifier = self.identifier_get(obj)
        path = self.dir / f'{identifier}.toml'
        if self.db.debug:
            print(f'Setting object {obj} at {path}')
        with open(path, 'w') as f:
            toml.dump(obj.dict(), f)
        return obj

    def get(self, name: str) -> T:
        identifier = name_fix(name)
        path = self.dir / f'{identifier}.toml'
        if self.db.debug:
            print(f'Getting object with identifier {identifier} from {path}')
        if not path.exists():
            raise ObjNotFound(
                f'{self.model.__name__} with name {identifier} not found.'
            )
        with open(path, 'r') as f:
            data = toml.load(f)
        return self.model(**data)

    def delete(self, name: str) -> None:
        identifier = name_fix(name)
        path = self.dir / f'{identifier}.toml'
        if self.db.debug:
            print(f'Deleting object with identifier {identifier} from {path}')
        if not path.exists():
            raise ObjNotFound(
                f'{self.model.__name__} with name {identifier} not found.'
            )
        path.unlink()

    def list(self) -> List[str]:
        if not self.dir.exists():
            raise FileNotFoundError(
                f'Directory {self.dir} does not exist for {self.model.__name__}.'
            )
        # expanded_path = Path(os.path.expanduser(self.dir)).resolve()
        files = [f.stem for f in self.dir.glob('*.toml')]
        if self.db.debug:
            print(f'Listing all objects in {self.dir}: {files}')
        return files


class DB:
    def __init__(self, base_dir: str, reset: bool = False, debug: bool = True):
        base_dir = os.path.expanduser(base_dir)
        self.base_dir = Path(base_dir)
        self.debug = debug
        if self.debug:
            print(
                f'Initializing database at {self.base_dir} with reset={reset}'
            )
        if reset:
            self.reset_database()

        self.user = DBCat(self, 'users', User)
        self.group = DBCat(self, 'groups', Group)
        self.info = DBCat(self, 'info', InfoPointer)
        self.acl = DBCat(self, 'acls', ACL)

    def reset_database(self):
        if self.base_dir.exists():
            if self.debug:
                print(f'Resetting database at {self.base_dir}')
            shutil.rmtree(self.base_dir)

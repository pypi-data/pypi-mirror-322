import datetime
import os
import yaml
import uuid
import json
import hashlib
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, StrictStr, Field
from sqlalchemy.ext.declarative import declarative_base
from osis.datatools import normalize_email, normalize_phone
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    TIMESTAMP,
    func,
    Boolean,
    Date,
    inspect,
    text,
    bindparam,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB, JSON
import logging
from termcolor import colored
from osis.db import DB, DBType  # type: ignore

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def calculate_months(
    investment_date: datetime.date, conversion_date: datetime.date
) -> float:
    delta = conversion_date - investment_date
    days_in_month = 30.44
    months = delta.days / days_in_month
    return months


def indexed_field(cls):
    cls.__index_fields__ = dict()
    for name, field in cls.__fields__.items():
        if field.json_schema_extra is not None:
            for cat in ["index", "indexft", "indexphone", "indexemail", "human"]:
                if field.json_schema_extra.get(cat, False):
                    if name not in cls.__index_fields__:
                        cls.__index_fields__[name] = dict()
                    # print(f"{cls.__name__} found index name:{name} cat:{cat}")
                    cls.__index_fields__[name][cat] = field.annotation
                    if cat in ["indexphone", "indexemail"]:
                        cls.__index_fields__[name]["indexft"] = field.annotation

    return cls


@indexed_field
class MyBaseModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: StrictStr = Field(default="", index=True, human=True)
    description: StrictStr = Field(default="")
    lasthash: StrictStr = Field(default="")
    creation_date: int = Field(
        default_factory=lambda: int(datetime.datetime.now().timestamp())
    )
    mod_date: int = Field(
        def ault_factory=lambda: int(datetime.datetime.now().timestamp())
    )

    def pre_save(self):
        self.mod_date = int(datetime.datetime.now().timestamp())
        print("pre-save")
        # for fieldname, typedict in self.__class__.__index_fields__.items():
        #     v= self.__dict__[fieldname]
        #     if 'indexphone' in typedict:
        #         self.__dict__[fieldname]=[normalize_phone(i) for i in v.split(",")].uniq()
        #     if 'indexemail' in typedict:
        #         self.__dict__[fieldname]=[normalize_email(i) for i in v.split(",")].uniq()

        # return ",".join(emails)

        #     print(field)
        #     #if field not in ["id", "name","creation_date", "mod_date"]:
        # from IPython import embed; embed()

    def yaml_get(self) -> str:
        data = self.dict()
        return yaml.dump(data, sort_keys=True, default_flow_style=False)

    def json_get(self) -> str:
        data = self.dict()
        # return self.model_dump_json()
        return json.dumps(data, sort_keys=True, indent=2)

    def hash(self) -> str:
        data = self.dict()
        data.pop("lasthash")
        data.pop("mod_date")
        data.pop("creation_date")
        data.pop("id")
        yaml_string = yaml.dump(data, sort_keys=True, default_flow_style=False)
        # Encode the YAML string to bytes using UTF-8 encoding
        yaml_bytes = yaml_string.encode("utf-8")
        self.lasthash = hashlib.md5(yaml_bytes).hexdigest()
        return self.lasthash

    def doc_id(self, partition: str) -> str:
        return f"{partition}:{self.id}"

    def __str__(self):
        return self.json_get()


T = TypeVar("T", bound=MyBaseModel)


class MyBaseFactory(Generic[T]):
    def __init__(
        self,
        model_cls: type[T],
        db: DB,
        use_fs: bool = True,
        keep_history: bool = False,
        reset: bool = False,
        load: bool = False,
        human_readable: bool = True,
    ):
        self.mycat = model_cls.__name__.lower()
        self.description = ""
        self.model_cls = model_cls
        self.engine = create_engine(db.cfg.url())
        self.Session = sessionmaker(bind=self.engine)
        self.use_fs = use_fs
        self.human_readable = human_readable
        self.keep_history = keep_history
        self.db = db
        dbcat = db.dbcat_new(cat=self.mycat, reset=reset)
        self.db_cat = dbcat
        self.ft_table_name = f"{self.mycat}_ft"

        self._init_db_schema(reset=reset)

        if self.use_fs:
            self._check_db_schema()
        else:
            if not self._check_db_schema_ok():
                raise RuntimeError(
                    "DB schema changed in line to model used, need to find ways how to migrate"
                )

        if reset:
            self.db_cat.reset()
            self._reset_db()

        if load:
            self.load()

    def _reset_db(self):
        logger.info(colored("Resetting database...", "red"))
        with self.engine.connect() as connection:
            cascade = ""
            if self.db.cfg.db_type == DBType.POSTGRESQL:
                cascade = " CASCADE"
            connection.execute(text(f'DROP TABLE IF EXISTS "{self.mycat}"{cascade}'))
            if self.keep_history:
                connection.execute(
                    text(f'DROP TABLE IF EXISTS "{self.mycat}_history" {cascade}')
                )
            connection.commit()
        self._init_db_schema()

    def _init_db_schema(self, reset: bool = False):
        # first make sure table is created if needed
        inspector = inspect(self.engine)
        if inspector.has_table(self.mycat):
            if reset:
                self._reset_db()
                return
            print(f"Table {self.mycat} does exist.")

        Base = declarative_base()

        def create_model(tablename):
            class MyModel(Base):
                __tablename__ = tablename
                id = Column(String, primary_key=True)
                name = Column(String, index=True)
                creation_date = Column(Integer, index=True)
                mod_date = Column(Integer, index=True)
                hash = Column(String, index=True)
                data = Column(JSON)
                version = Column(Integer)
                index_fields = self.model_cls.__index_fields__
                for field, index_types in index_fields.items():
                    if "index" in index_types:
                        field_type = index_types["index"]
                        if field not in ["id", "name", "creation_date", "mod_date"]:
                            if field_type == int:
                                locals()[field] = Column(Integer, index=True)
                            elif field_type == datetime.date:
                                locals()[field] = Column(Date, index=True)
                            elif field_type == bool:
                                locals()[field] = Column(Boolean, index=True)
                            else:
                                locals()[field] = Column(String, index=True)

            create_model_ft()
            return MyModel

        def create_model_ft():
            index_fields = self.model_cls.__index_fields__
            toindex: List[str] = []
            for fieldnam, index_types in index_fields.items():
                print(f"field name: {fieldnam}")
                print(f"toindex: {toindex}")
                if "indexft" in index_types:
                    toindex.append(fieldnam)
            if len(toindex) > 0:
                with self.engine.connect() as connection:
                    result = connection.execute(
                        text(
                            "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"
                        ),
                        {"table_name": self.ft_table_name},
                    )
                    if result.fetchone() is None:
                        # means table does not exist
                        st = text(
                            "CREATE VIRTUAL TABLE :table_name USING fts5(:fields)"
                        )
                        st = st.bindparams(bindparam("fields", expanding=True))
                        st = st.bindparams(
                            table_name=self.ft_table_name, fields=toindex
                        )
                        # TODO: this is not working
                        connection.execute(
                            st,
                            {
                                "table_name": self.ft_table_name,
                                "fields": toindex,
                            },
                        )

        self.table_model = create_model(self.mycat)

        if self.keep_history:
            self.history_table_model = create_model(
                "HistoryTableModel", f"{self.mycat}_history"
            )

        Base.metadata.create_all(self.engine)

    def _check_db_schema_ok(self) -> bool:

        inspector = inspect(self.engine)
        table_name = self.table_model.__tablename__

        # Get columns from the database
        db_columns = {col["name"]: col for col in inspector.get_columns(table_name)}

        # Get columns from the model
        model_columns = {c.name: c for c in self.table_model.__table__.columns}

        # print("model col")
        # print(model_columns)

        # Check for columns in model but not in db
        for col_name, col in model_columns.items():
            if col_name not in db_columns:
                logger.info(
                    colored(
                        f"Column '{col_name}' exists in model but not in database",
                        "red",
                    )
                )
                return False
            else:
                # Check column type
                db_col = db_columns[col_name]
                if str(col.type) != str(db_col["type"]):
                    logger.info(
                        colored(
                            f"Column '{col_name}' type mismatch: Model {col.type}, DB {db_col['type']}",
                            "red",
                        )
                    )
                    return False

        # Check for columns in db but not in model
        for col_name in db_columns:
            if col_name not in model_columns:
                logger.info(
                    colored(
                        f"Column '{col_name}' exists in database but not in model",
                        "red",
                    )
                )
                return False
        return True

    def _check_db_schema(self):
        # check if schema is ok, if not lets reload
        if self._check_db_schema_ok():
            return
        self.load()

    def new(self, name: str = "", **kwargs) -> T:
        o = self.model_cls(name=name, **kwargs)
        return o

    def _encode(self, item: T) -> dict:
        return item.model_dump()

    def _decode(self, data: str) -> T:
        if self.use_fs:
            return self.model_cls(**yaml.load(data, Loader=yaml.Loader))
        else:
            return self.model_cls(**json.loads(data))

    def get(self, id: str = "") -> T:
        if not isinstance(id, str):
            raise ValueError(f"id needs to be str. Now: {id}")
        session = self.Session()
        result = session.query(self.table_model).filter_by(id=id).first()
        session.close()
        if result:
            if self.use_fs:
                data = self.db_cat.get(id=id)
            else:
                data = result.data
            return self._decode(data)
        raise ValueError(f"can't find {self.mycat}:{id}")

    def exists(self, id: str = "") -> bool:
        if not isinstance(id, str):
            raise ValueError(f"id needs to be str. Now: {id}")
        session = self.Session()
        result = session.query(self.table_model).filter_by(id=id).first()
        session.close()
        return result is not None

    def get_by_name(self, name: str) -> Optional[T]:
        r = self.list(name=name)
        if len(r) > 1:
            raise ValueError(f"found more than 1 object with name {name}")
        if len(r) < 1:
            raise ValueError(f"object not found with name {name}")
        return r[0]

    def set(self, item: T, ignorefs: bool = False):

        item.pre_save()
        new_hash = item.hash()

        session = self.Session()
        db_item = session.query(self.table_model).filter_by(id=item.id).first()
        data = item.model_dump()

        index_fields = self.model_cls.__index_fields__
        to_ft_index = List[str]
        ft_field_values = [f"'{db_item.id}'"]
        for field_name, index_types in index_fields.items():
            if "indexft" in index_types:
                to_ft_index.append(field_name)
                ft_field_values.append(f"'{db_item[field_name]}'")

        if db_item:
            if db_item.hash != new_hash:
                db_item.name = item.name
                db_item.mod_date = item.mod_date
                db_item.creation_date = item.creation_date
                db_item.hash = new_hash
                if not self.use_fs:
                    db_item.data = data

                # Update indexed fields
                for field, val in self.model_cls.__indexed_fields__:  # type: ignore
                    if field not in ["id", "name", "creation_date", "mod_date"]:
                        if "indexft" in val:
                            session.execute(
                                f"UPDATE {self.ft_table_name} SET {field} = '{getattr(item, field)}'"
                            )

                        setattr(db_item, field, getattr(item, field))

                if self.keep_history and not self.use_fs:
                    version = (
                        session.query(func.max(self.history_table_model.version))
                        .filter_by(id=item.id)
                        .scalar()
                        or 0
                    )
                    history_item = self.history_table_model(
                        id=f"{item.id}_{version + 1}",
                        name=item.name,
                        creation_date=item.creation_date,
                        mod_date=item.mod_date,
                        hash=new_hash,
                        data=data,
                        version=version + 1,
                    )
                    session.add(history_item)

                if not ignorefs and self.use_fs:
                    self.db_cat.set(data=item.yaml_get(), id=item.id)
        else:
            db_item = self.table_model(
                id=item.id,
                name=item.name,
                creation_date=item.creation_date,
                mod_date=item.mod_date,
                hash=new_hash,
            )
            if not self.use_fs:
                db_item.data = item.json_get()
            session.add(db_item)

            session.execute(
                f'INSERT INTO {self.ft_table_name} (id, {", ".join(to_ft_index)}) VALUES ({", ".join(ft_field_values)})'
            )

            if not ignorefs and self.use_fs:
                self.db_cat.set(
                    data=item.yaml_get(), id=item.id, humanid=self._human_name_get(item)
                )

            # Set indexed fields
            for field, _ in self.model_cls.__indexed_fields__:  # type: ignore
                if field not in ["id", "name", "creation_date", "mod_date"]:
                    setattr(db_item, field, getattr(item, field))
            session.add(db_item)

        session.commit()
        session.close()

    # used for a symlink so its easy for a human to edit
    def _human_name_get(self, item: T) -> str:
        humanname = ""
        if self.human_readable:
            for fieldhuman, _ in self.model_cls.__human_fields__:  # type: ignore
                if fieldhuman not in ["id", "creation_date", "mod_date"]:
                    humanname += f"{item.__getattribute__(fieldhuman)}_"
            humanname = humanname.rstrip("_")
            if humanname == "":
                raise Exception(f"humanname should not be empty for {item}")
        return humanname

    def delete(self, id: str):
        if not isinstance(id, str):
            raise ValueError(f"id needs to be str. Now: {id}")
        session = self.Session()
        result = session.query(self.table_model).filter_by(id=id).delete()
        session.execute(f"DELETE FROM {self.ft_table_name} WHERE id={id};")
        session.commit()
        session.close()
        if result > 1:
            raise ValueError(f"multiple values deleted with id {id}")
        elif result == 0:
            raise ValueError(f"no record found with id {id}")

        if self.use_fs:
            humanid = ""
            if self.exists():
                item = self.get(id)
                # so we can remove the link
                humanid = self._human_name_get(item)
            self.db_cat.delete(id=id, humanid=humanid)

    def list(
        self, id: Optional[str] = None, name: Optional[str] = None, **kwargs
    ) -> List[T]:
        session = self.Session()
        query = session.query(self.table_model)
        if id:
            query = query.filter(self.table_model.id == id)
        if name:
            query = query.filter(self.table_model.name.ilike(f"%{name}%"))

        index_fields = self.model_cls.__index_fields__
        for key, value in kwargs.items():
            if value is None:
                continue
            if self.use_fs:
                query = query.filter(getattr(self.table_model, key) == value)
            else:
                if key in index_fields and "indexft" in index_fields[key]:
                    result = session.execute(
                        f'SELECT id From {self.ft_table_name} WHERE {key} MATCH "{value}"'
                    )

                    ids = []
                    for _, value in result:
                        ids.append(value)

                    query = query.filter(self.table_model.id in ids)
                else:
                    query = query.filter(
                        self.table_model.data[key].astext.ilike(f"%{value}%")
                    )
        results = query.all()
        session.close()

        items = []
        for result in results:
            items.append(self.get(id=result.id))

        return items

    def load(self, reset: bool = False):

        if self.use_fs:
            logger.info(colored(f"Reload DB.", "green"))
            if reset:
                self._reset_db()

            # Get all IDs and hashes from the database
            session = self.Session()
            db_items = {
                item.id: item.hash
                for item in session.query(
                    self.table_model.id, self.table_model.hash
                ).all()
            }
            session.close()

            done = []

            for root, _, files in os.walk(self.db.path):
                for file in files:
                    if file.endswith(".yaml"):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r") as f:
                            data = yaml.safe_load(f)
                            obj = self._decode(data)
                            myhash = obj.hash()

                            if reset:
                                self.set(obj, ignorefs=True)
                            else:
                                if obj.id in db_items:
                                    if db_items[obj.id] != myhash:
                                        # Hash mismatch, update the database record
                                        self.set(obj, ignorefs=True)
                                else:
                                    # New item, add to database
                                    self.set(obj, ignorefs=True)

                            done.append(obj.id)

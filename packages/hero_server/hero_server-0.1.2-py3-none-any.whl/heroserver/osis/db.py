import os
import shutil
import logging
from termcolor import colored
from herotools.pathtools import expand_path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from osis.id import int_to_id
from psycopg2.extras import DictCursor

import sqlite3
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class DBCat:
    def __init__(self, path: str, cat: str):
        path = expand_path(path)
        self.path_id = os.path.join(path, "id", cat)
        self.path_human = os.path.join(path, "human", cat)
        self.path = path
        self._init()

    def _init(self):
        os.makedirs(self.path_id, exist_ok=True)
        os.makedirs(self.path_human, exist_ok=True)

    def reset(self):
        if os.path.exists(self.path_id):
            shutil.rmtree(self.path_id, ignore_errors=True)
        if os.path.exists(self.path_human):
            shutil.rmtree(self.path_human, ignore_errors=True)
        self._init()

    def _get_path_id(self, id: str) -> str:
        id1 = id[:2]
        dir_path = os.path.join(self.path_id, id1)
        file_path = os.path.join(dir_path, f"{id}.yaml")
        os.makedirs(dir_path, exist_ok=True)
        return file_path

    def set(self, id: str, data: str, humanid: str = ""):
        fs_path = self._get_path_id(id=id)
        with open(fs_path, "w") as f:
            f.write(data)
        if humanid != "":
            human_file_path = os.path.join(self.path_human, humanid)
            # Create a symbolic link
            try:
                os.symlink(fs_path, human_file_path)
            except FileExistsError:
                # If the symlink already exists, we can either ignore it or update it
                if not os.path.islink(human_file_path):
                    raise  # If it's not a symlink, re-raise the exception
                os.remove(human_file_path)  # Remove the existing symlink
                os.symlink(fs_path, human_file_path)  # Create a new symlink
        return fs_path

    def get(self, id: str) -> str:
        fs_path = self._get_path_id(id=id)
        with open(fs_path, "r") as f:
            return f.read()

    def delete(self, id: str, humanid: str = ""):
        fs_path = self._get_path_id(id=id)
        os.remove(fs_path)
        if humanid != "":
            human_file_path = os.path.join(self.path_human, humanid)
            os.remove(human_file_path)

class DBType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"

class DBConfig:
    def __init__(
        self,
        db_type: DBType = DBType.POSTGRESQL,
        db_name: str = "main",
        db_login: str = "admin",
        db_passwd: str = "admin",
        db_addr: str = "localhost",
        db_port: int = 5432,
        db_path: str = "/tmp/db"
    ):
        self.db_type = db_type
        self.db_name = db_name
        self.db_login = db_login
        self.db_passwd = db_passwd
        self.db_addr = db_addr
        self.db_port = db_port
        self.db_path = expand_path(db_path)

    def __str__(self):
        return (f"DBConfig(db_name='{self.db_name}', db_login='{self.db_login}', "
                f"db_addr='{self.db_addr}', db_port={self.db_port}, db_path='{self.db_path}')")

    def __repr__(self):
        return self.__str__()
    
    
    def url(self) -> str:
        if self.db_type == DBType.POSTGRESQL:
            return f"postgresql://{self.db_login}:{self.db_passwd}@{self.db_addr}:{self.db_port}/{self.db_name}"
        elif self.db_type == DBType.SQLITE:
            return f"sqlite:///{self.db_path}/{self.db_name}.db"
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
    
class DB:
    def __init__(self,cfg:DBConfig , path: str, reset: bool = False):
        self.cfg = cfg
        self.path = expand_path(path)
        self.path_id = os.path.join(self.path, "id")
        self.path_human = os.path.join(self.path, "human")
        self.dbcats = dict[str, DBCat]()
        
        if reset:
            self.reset()
        else:
            self._init()

    def reset(self):
        if os.path.exists(self.path_id):
            shutil.rmtree(self.path_id, ignore_errors=True)
            logger.info(colored(f"Removed db dir: {self.path_id}", "red"))
        if os.path.exists(self.path_human):
            shutil.rmtree(self.path_human, ignore_errors=True)
            logger.info(colored(f"Removed db dir: {self.path_human}", "red"))   
            if self.cfg.db_type == DBType.POSTGRESQL:
                conn=self.db_connection()    
                cur = conn.cursor() 
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.cfg.db_name,))
                exists = cur.fetchone()
                cur.close()
                conn.close()
                if exists:
                    # Disconnect from the current database
                    # Reconnect to the postgres database to drop the target database
                    conn = psycopg2.connect(dbname='postgres', user=self.cfg.db_login, password=self.cfg.db_passwd, host=self.cfg.db_addr)
                    conn.autocommit = True
                    cur = conn.cursor()
                    #need to remove the open connections to be able to remove it
                    cur.execute(f"""
                        SELECT pg_terminate_backend(pg_stat_activity.pid)
                        FROM pg_stat_activity
                        WHERE pg_stat_activity.datname = %s
                        AND pid <> pg_backend_pid();
                    """, (self.cfg.db_name,))
                    print(f"Terminated all connections to database '{self.cfg.db_name}'")
                        
                    cur.execute(f"DROP DATABASE {self.cfg.db_name}")
                    print(f"Database '{self.cfg.db_name}' dropped successfully.")            
                    cur.close()
                    conn.close()
    
        self._init()

    def _init(self):
        os.makedirs(self.path_human, exist_ok=True)
        os.makedirs(self.path_id, exist_ok=True)
        for key, dbcat in self.dbcats:
            dbcat._init()

    def dbcat_new(self, cat: str, reset: bool = False) -> DBCat:
        dbc = DBCat(cat=cat, path=self.path)
        self.dbcats[cat] = dbc
        return dbc

    def dbcat_get(self, cat: str) -> DBCat:
        if cat in self.dbcats:
            return self.dbcats[cat]
        raise Exception(f"can't find dbcat with cat:{cat}")

    def db_connection(self):
        if self.cfg.db_type == DBType.POSTGRESQL:
            try:
                conn = psycopg2.connect(
                    dbname=self.cfg.db_name,
                    user=self.cfg.db_login,
                    password=self.cfg.db_passwd,
                    host=self.cfg.db_addr,
                    port=self.cfg.db_port 
                )
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                conn.autocommit = True  # Set autocommit mode     
            except psycopg2.OperationalError as e:
                if f"database \"{self.cfg.db_name}\" does not exist" in str(e):
                    # Connect to 'postgres' database to create the new database
                    conn = psycopg2.connect(
                        dbname='postgres',
                        user=self.cfg.db_login,
                        password=self.cfg.db_passwd,
                        host=self.cfg.db_addr,
                        port=self.cfg.db_port 
                    )
                    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                    cur = conn.cursor()
                    cur.execute(f"CREATE DATABASE {self.cfg.db_name}")
                    cur.close()
                    conn.close()
                    
                    # Now connect to the newly created database
                    conn = psycopg2.connect(
                        dbname=self.cfg.db_name,
                        user=self.cfg.db_login,
                        password=self.cfg.db_passwd,
                        host=self.cfg.db_addr,
                        port=self.cfg.db_port 
                    )
                    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                    print(f"Database '{self.cfg.db_name}' created successfully.")
                else:
                    raise e
        elif self.cfg.db_type == DBType.SQLITE:
            db_file = os.path.join(self.cfg.db_path, f"{self.cfg.db_name}.db")
            conn = sqlite3.connect(db_file)
        else:
            raise ValueError(f"Unsupported database type: {self.cfg.db_type}")
        return conn

    def db_create(self, db_name: str = "", user_name: str = "", user_password: str = ""):
        if self.cfg.db_type == DBType.POSTGRESQL:
            self.db_create_id()
            # Connect to PostgreSQL server
            conn = self.db_connection()
            cur = conn.cursor()
            
            if db_name=="":
                db_name=self.cfg.db_name

            try:
                # Check if the database already exists
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                exists = cur.fetchone()

                if not exists:
                    # Create the database
                    cur.execute(f"CREATE DATABASE {db_name}")
                    print(f"Database '{db_name}' created successfully.")

                    if user_name and user_password:
                        # Check if user exists
                        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (user_name,))
                        user_exists = cur.fetchone()

                        if not user_exists:
                            # Create the user
                            cur.execute(f"CREATE USER {user_name} WITH PASSWORD %s", (user_password,))
                            print(f"User '{user_name}' created successfully.")

                        # Grant privileges on the database to the user
                        cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user_name}")
                        print(f"Privileges granted to '{user_name}' on '{db_name}'.")

            except psycopg2.Error as e:
                raise Exception(f"Postgresql error: {e}")
            finally:
                # Close the cursor and connection
                cur.close()
                conn.close()

        elif self.cfg.db_type == DBType.SQLITE:
            # For SQLite, we just need to create the database file if it doesn't exist
            db_file = os.path.join(self.cfg.db_path, f"{db_name}.db")
            if not os.path.exists(db_file):
                conn = sqlite3.connect(db_file)
                conn.close()
                print(f"SQLite database '{db_name}' created successfully at {db_file}.")
            else:
                print(f"SQLite database '{db_name}' already exists at {db_file}.")

            if user_name:
                print("Note: SQLite doesn't support user management like PostgreSQL.")

        else:
            raise ValueError(f"Unsupported database type: {self.cfg.db_type}")


    def db_create_id(self):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_id_counters (
                        user_id INTEGER PRIMARY KEY,
                        last_id_given INTEGER NOT NULL DEFAULT 0
                    )
                """)
            conn.commit()


    def new_id(self,user_id: int) -> str:
        if not 0 <= user_id <= 50:
            raise ValueError("User ID must be between 0 and 50")

        max_ids = 60466175
        ids_per_user = max_ids // 51  # We use 51 to ensure we don't exceed the max even for user_id 50

        with self.db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                # Try to get the last_id_given for this user
                cur.execute("SELECT last_id_given FROM user_id_counters WHERE user_id = %s", (user_id,))
                result = cur.fetchone()

                if result is None:
                    # If no record exists for this user, insert a new one
                    cur.execute(
                        "INSERT INTO user_id_counters (user_id, last_id_given) VALUES (%s, 0) RETURNING last_id_given",
                        (user_id,)
                    )
                    last_id_given = 0
                else:
                    last_id_given = result['last_id_given']

                # Calculate the new ID
                new_id_int = (user_id * ids_per_user) + last_id_given + 1

                if new_id_int > (user_id + 1) * ids_per_user:
                    raise ValueError(f"No more IDs available for user {user_id}")

                # Update the last_id_given in the database
                cur.execute(
                    "UPDATE user_id_counters SET last_id_given = last_id_given + 1 WHERE user_id = %s",
                    (user_id,)
                )
                conn.commit()

        return int_to_id(new_id_int)    
            
        

def db_new(
    db_type: DBType = DBType.POSTGRESQL,
    db_name: str = "main",
    db_login: str = "admin",
    db_passwd: str = "admin",
    db_addr: str = "localhost",
    db_port: int = 5432,
    db_path: str = "/tmp/db",
    reset: bool = False,
):
    # Create a DBConfig object
    config = DBConfig(
        db_type=db_type,
        db_name=db_name,
        db_login=db_login,
        db_passwd=db_passwd,
        db_addr=db_addr,
        db_port=db_port,
        db_path=db_path
    )
    
    # Create and return a DB object
    mydb =  DB(cfg=config, path=db_path, reset=reset)
    mydb.db_create()
    return mydb



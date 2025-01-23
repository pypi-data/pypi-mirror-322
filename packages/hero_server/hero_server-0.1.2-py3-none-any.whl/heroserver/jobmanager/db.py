import os

from peewee import *

from .models import MODELS, database


class DB:
    def __init__(self, db_type="sqlite", **kwargs):
        """Initialize database connection using Peewee ORM.

        Args:
            db_type: Type of database ('sqlite' or 'postgresql'). Defaults to 'sqlite'.
            **kwargs: Database-specific connection parameters
                For SQLite:
                    - db_path: Path to SQLite database file. Defaults to /tmp/jobdb.sqlite
                    - pragmas: SQLite pragmas. Defaults to {'journal_mode': 'wal', 'foreign_keys': 1}
                For PostgreSQL:
                    - host: Database host. Defaults to localhost
                    - port: Database port. Defaults to 5432
                    - dbname: Database name. Defaults to postgres
                    - user: Database user. Defaults to postgres
                    - password: Database password. Defaults to admin

        Raises:
            Exception: If database initialization fails
        """
        try:
            if db_type == "sqlite":
                self._init_sqlite(**kwargs)
            elif db_type == "postgresql":
                self._init_postgresql(**kwargs)
            else:
                raise ValueError(f"Unsupported database type: {db_type}")

            # Initialize tables
            self._init_tables()

        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            if hasattr(self, "db"):
                self.db.close()
            raise

    def _init_sqlite(self, db_path="/tmp/jobdb.sqlite", pragmas=None):
        """Initialize SQLite database connection."""
        if pragmas is None:
            pragmas = {"journal_mode": "wal", "foreign_keys": 1}

        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            if not os.access(db_dir, os.W_OK):
                raise OSError(f"No write access to directory: {db_dir}")

        self.db = SqliteDatabase(db_path, pragmas=pragmas)
        database.initialize(self.db)
        print(f"SQLite database initialized at {db_path}")

    def _init_postgresql(self, host="localhost", port=5432, dbname="postgres", user="postgres", password="admin"):
        """Initialize PostgreSQL database connection."""
        self.db = PostgresqlDatabase(dbname, user=user, password=password, host=host, port=port)
        database.initialize(self.db)
        print(f"PostgreSQL database initialized at {host}:{port}/{dbname}")

    def _init_tables(self):
        """Create tables if they don't exist."""
        with self.db:
            self.db.create_tables(MODELS)
        print("Database tables created successfully")

    def __del__(self):
        """Ensure database connection is closed."""
        if hasattr(self, "db"):
            self.db.close()

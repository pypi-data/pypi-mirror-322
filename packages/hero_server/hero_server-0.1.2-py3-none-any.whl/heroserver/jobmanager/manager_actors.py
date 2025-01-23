import sqlite3
from typing import List, Optional

from heroserver.db import DB
from heroserver.models import Actor, Executor


class ManagerActors:
    def __init__(self, db: DB):
        self.db = DB

    def add(self, name: str, executor: Executor, description: Optional[str] = None) -> int:
        """Add a new actor.

        Args:
            name: Name of the actor
            executor: Executor instance this actor belongs to
            description: Optional description of the actor

        Returns:
            int: ID of the created actor
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    INSERT INTO actor (name, executor_id, description)
                    VALUES (?, ?, ?)
                    """,
                    (name, executor.id, description),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding actor: {e}")
            raise

    def get(self, actor_id: int) -> Optional[Actor]:
        """Get an actor by ID.

        Args:
            actor_id: ID of the actor to get

        Returns:
            Optional[Actor]: Actor if found, None otherwise
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    SELECT a.*, e.name as executor_name, e.description as executor_description, e.state as executor_state
                    FROM actor a
                    JOIN executor e ON a.executor_id = e.id
                    WHERE a.id = ?
                    """,
                    (actor_id,),
                )
                row = cursor.fetchone()
                if row:
                    executor = Executor(
                        id=row["executor_id"],
                        name=row["executor_name"],
                        description=row["executor_description"],
                        state=row["executor_state"],
                    )
                    return Actor(id=row["id"], name=row["name"], executor=executor, description=row["description"])
                return None
        except sqlite3.Error as e:
            print(f"Error getting actor: {e}")
            raise

    def get_by_name(self, name: str) -> Optional[Actor]:
        """Get an actor by name.

        Args:
            name: Name of the actor to get

        Returns:
            Optional[Actor]: Actor if found, None otherwise
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    SELECT a.*, e.name as executor_name, e.description as executor_description, e.state as executor_state
                    FROM actor a
                    JOIN executor e ON a.executor_id = e.id
                    WHERE a.name = ?
                    """,
                    (name,),
                )
                row = cursor.fetchone()
                if row:
                    executor = Executor(
                        id=row["executor_id"],
                        name=row["executor_name"],
                        description=row["executor_description"],
                        state=row["executor_state"],
                    )
                    return Actor(id=row["id"], name=row["name"], executor=executor, description=row["description"])
                return None
        except sqlite3.Error as e:
            print(f"Error getting actor by name: {e}")
            raise

    def list(self, executor_id: Optional[int] = None) -> List[Actor]:
        """List all actors, optionally filtered by executor.

        Args:
            executor_id: Optional executor ID to filter by

        Returns:
            List[Actor]: List of actors
        """
        sql = """
        SELECT a.*, e.name as executor_name, e.description as executor_description, e.state as executor_state
        FROM actor a
        JOIN executor e ON a.executor_id = e.id
        """
        params = []

        if executor_id is not None:
            sql += " WHERE a.executor_id = ?"
            params.append(executor_id)

        sql += " ORDER BY a.name"

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                actors = []
                for row in cursor:
                    executor = Executor(
                        id=row["executor_id"],
                        name=row["executor_name"],
                        description=row["executor_description"],
                        state=row["executor_state"],
                    )
                    actors.append(Actor(id=row["id"], name=row["name"], executor=executor, description=row["description"]))
                return actors
        except sqlite3.Error as e:
            print(f"Error listing actors: {e}")
            raise

    def update(self, actor_id: int, name: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Update an actor's details.

        Args:
            actor_id: ID of the actor to update
            name: Optional new name
            description: Optional new description

        Returns:
            bool: True if actor was updated, False if actor not found
        """
        if name is None and description is None:
            return False

        sql = "UPDATE actor SET"
        params = []
        updates = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)

        sql += " " + ", ".join(updates)
        sql += " WHERE id = ?"
        params.append(actor_id)

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating actor: {e}")
            raise

    def delete(self, actor_id: int) -> bool:
        """Delete an actor.

        Args:
            actor_id: ID of the actor to delete

        Returns:
            bool: True if actor was deleted, False if actor not found
        """
        try:
            with self.conn:
                cursor = self.conn.execute("DELETE FROM actor WHERE id = ?", (actor_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting actor: {e}")
            raise

    def delete_all(self) -> int:
        """Delete all actors.

        Returns:
            int: Number of actors deleted
        """
        try:
            with self.conn:
                cursor = self.conn.execute("DELETE FROM actor")
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error deleting all actors: {e}")
            raise

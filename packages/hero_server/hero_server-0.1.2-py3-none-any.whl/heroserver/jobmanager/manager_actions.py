import sqlite3
from typing import List, Optional

from heroserver.db import DB
from heroserver.models import Action, Actor


class ManagerActions:
    def __init__(self, db: DB):
        self.db = DB

    def add(self, name: str, actor: Actor, description: Optional[str] = None, code: Optional[str] = None) -> int:
        """Add a new action.

        Args:
            name: Name of the action
            actor: Actor instance this action belongs to
            description: Optional description of the action
            code: Optional code implementation of the action

        Returns:
            int: ID of the created action
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    INSERT INTO action (name, actor_id, description, code, nrok, nrfailed)
                    VALUES (?, ?, ?, ?, 0, 0)
                    """,
                    (name, actor.id, description, code),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding action: {e}")
            raise

    def get(self, action_id: int) -> Optional[Action]:
        """Get an action by ID.

        Args:
            action_id: ID of the action to get

        Returns:
            Optional[Action]: Action if found, None otherwise
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    SELECT a.*, ac.name as actor_name, ac.description as actor_description,
                           ac.executor_id
                    FROM action a
                    JOIN actor ac ON a.actor_id = ac.id
                    WHERE a.id = ?
                    """,
                    (action_id,),
                )
                row = cursor.fetchone()
                if row:
                    actor = Actor(
                        id=row["actor_id"], name=row["actor_name"], description=row["actor_description"], executor_id=row["executor_id"]
                    )
                    return Action(
                        id=row["id"],
                        name=row["name"],
                        actor=actor,
                        description=row["description"],
                        code=row["code"],
                        nrok=row["nrok"],
                        nrfailed=row["nrfailed"],
                    )
                return None
        except sqlite3.Error as e:
            print(f"Error getting action: {e}")
            raise

    def get_by_name(self, actor_id: int, name: str) -> Optional[Action]:
        """Get an action by name within an actor.

        Args:
            actor_id: ID of the actor
            name: Name of the action

        Returns:
            Optional[Action]: Action if found, None otherwise
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    SELECT a.*, ac.name as actor_name, ac.description as actor_description,
                           ac.executor_id
                    FROM action a
                    JOIN actor ac ON a.actor_id = ac.id
                    WHERE a.actor_id = ? AND a.name = ?
                    """,
                    (actor_id, name),
                )
                row = cursor.fetchone()
                if row:
                    actor = Actor(
                        id=row["actor_id"], name=row["actor_name"], description=row["actor_description"], executor_id=row["executor_id"]
                    )
                    return Action(
                        id=row["id"],
                        name=row["name"],
                        actor=actor,
                        description=row["description"],
                        code=row["code"],
                        nrok=row["nrok"],
                        nrfailed=row["nrfailed"],
                    )
                return None
        except sqlite3.Error as e:
            print(f"Error getting action by name: {e}")
            raise

    def list(self, actor_id: Optional[int] = None) -> List[Action]:
        """List all actions, optionally filtered by actor.

        Args:
            actor_id: Optional actor ID to filter by

        Returns:
            List[Action]: List of actions
        """
        sql = """
        SELECT a.*, ac.name as actor_name, ac.description as actor_description,
               ac.executor_id
        FROM action a
        JOIN actor ac ON a.actor_id = ac.id
        """
        params = []

        if actor_id is not None:
            sql += " WHERE a.actor_id = ?"
            params.append(actor_id)

        sql += " ORDER BY a.name"

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                actions = []
                for row in cursor:
                    actor = Actor(
                        id=row["actor_id"], name=row["actor_name"], description=row["actor_description"], executor_id=row["executor_id"]
                    )
                    actions.append(
                        Action(
                            id=row["id"],
                            name=row["name"],
                            actor=actor,
                            description=row["description"],
                            code=row["code"],
                            nrok=row["nrok"],
                            nrfailed=row["nrfailed"],
                        )
                    )
                return actions
        except sqlite3.Error as e:
            print(f"Error listing actions: {e}")
            raise

    def update(self, action_id: int, name: Optional[str] = None, description: Optional[str] = None, code: Optional[str] = None) -> bool:
        """Update an action's details.

        Args:
            action_id: ID of the action to update
            name: Optional new name
            description: Optional new description
            code: Optional new code implementation

        Returns:
            bool: True if action was updated, False if action not found
        """
        if name is None and description is None and code is None:
            return False

        sql = "UPDATE action SET"
        params = []
        updates = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if code is not None:
            updates.append("code = ?")
            params.append(code)

        sql += " " + ", ".join(updates)
        sql += " WHERE id = ?"
        params.append(action_id)

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating action: {e}")
            raise

    def increment_success(self, action_id: int) -> bool:
        """Increment the success counter for an action.

        Args:
            action_id: ID of the action

        Returns:
            bool: True if counter was incremented, False if action not found
        """
        try:
            with self.conn:
                cursor = self.conn.execute("UPDATE action SET nrok = nrok + 1 WHERE id = ?", (action_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error incrementing success counter: {e}")
            raise

    def increment_failure(self, action_id: int) -> bool:
        """Increment the failure counter for an action.

        Args:
            action_id: ID of the action

        Returns:
            bool: True if counter was incremented, False if action not found
        """
        try:
            with self.conn:
                cursor = self.conn.execute("UPDATE action SET nrfailed = nrfailed + 1 WHERE id = ?", (action_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error incrementing failure counter: {e}")
            raise

    def delete(self, action_id: int) -> bool:
        """Delete an action.

        Args:
            action_id: ID of the action to delete

        Returns:
            bool: True if action was deleted, False if action not found
        """
        try:
            with self.conn:
                cursor = self.conn.execute("DELETE FROM action WHERE id = ?", (action_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting action: {e}")
            raise

    def delete_all(self) -> int:
        """Delete all actions.

        Returns:
            int: Number of actions deleted
        """
        try:
            with self.conn:
                cursor = self.conn.execute("DELETE FROM action")
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error deleting all actions: {e}")
            raise

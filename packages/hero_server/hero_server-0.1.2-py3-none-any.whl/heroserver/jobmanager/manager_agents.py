import sqlite3
from typing import List, Optional

from heroserver.db import DB
from heroserver.models import Agent, SignatureRequest


class ManagerAgents:
    def __init__(self, db: DB):
        self.db = DB

    # Agent operations
    def set(self, agent: Agent) -> int:
        """Add or update an agent.

        Args:
            agent: Agent instance to add/update

        Returns:
            int: ID of the agent
        """
        try:
            with self.conn:
                if agent.id:
                    # Update existing agent
                    self.conn.execute(
                        """
                        UPDATE agent 
                        SET name = ?, description = ?, ipaddr = ?, 
                            pubkey = ?, location = ?
                        WHERE id = ?
                        """,
                        (agent.name, agent.description, agent.ipaddr, agent.pubkey, agent.location, agent.id),
                    )
                    return agent.id
                else:
                    # Insert new agent
                    cursor = self.conn.execute(
                        """
                        INSERT INTO agent 
                        (name, description, ipaddr, pubkey, location, create_date)
                        VALUES (?, ?, ?, ?, ?, strftime('%s', 'now'))
                        """,
                        (agent.name, agent.description, agent.ipaddr, agent.pubkey, agent.location),
                    )
                    return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error setting agent: {e}")
            raise

    def get(self, agent_id: int) -> Optional[Agent]:
        """Get an agent by ID.

        Args:
            agent_id: ID of the agent to retrieve

        Returns:
            Optional[Agent]: Agent instance if found, None otherwise
        """
        try:
            with self.conn:
                # Get agent data
                cursor = self.conn.execute("SELECT * FROM agent WHERE id = ?", (agent_id,))
                row = cursor.fetchone()
                if not row:
                    return None

                # Get signature requests for this agent
                cursor = self.conn.execute("SELECT * FROM signature_requests WHERE agent_id = ? ORDER BY date DESC", (agent_id,))
                signatures = [
                    SignatureRequest(
                        id=sig_row["id"],
                        pubkey=sig_row["pubkey"],
                        signature=sig_row["signature"],
                        date=sig_row["date"],
                        verified=bool(sig_row["verified"]),
                    )
                    for sig_row in cursor.fetchall()
                ]

                return Agent(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    ipaddr=row["ipaddr"],
                    pubkey=row["pubkey"],
                    location=row["location"],
                    create_date=row["create_date"],
                    signatures=signatures,
                )
        except sqlite3.Error as e:
            print(f"Error getting agent: {e}")
            raise

    def list(self) -> List[Agent]:
        """List all agents.

        Returns:
            List[Agent]: List of all agents with their signature requests
        """
        try:
            with self.conn:
                cursor = self.conn.execute("SELECT * FROM agent ORDER BY name")
                agents = []
                for row in cursor:
                    # Get signature requests for this agent
                    sig_cursor = self.conn.execute("SELECT * FROM signature_requests WHERE agent_id = ? ORDER BY date DESC", (row["id"],))
                    signatures = [
                        SignatureRequest(
                            id=sig_row["id"],
                            pubkey=sig_row["pubkey"],
                            signature=sig_row["signature"],
                            date=sig_row["date"],
                            verified=bool(sig_row["verified"]),
                        )
                        for sig_row in sig_cursor.fetchall()
                    ]

                    agents.append(
                        Agent(
                            id=row["id"],
                            name=row["name"],
                            description=row["description"],
                            ipaddr=row["ipaddr"],
                            pubkey=row["pubkey"],
                            location=row["location"],
                            create_date=row["create_date"],
                            signatures=signatures,
                        )
                    )
                return agents
        except sqlite3.Error as e:
            print(f"Error listing agents: {e}")
            raise

    def delete(self, agent_id: int) -> int:
        """Delete an agent and all its associated signature requests.

        Args:
            agent_id: ID of the agent to delete

        Returns:
            int: Number of agents deleted (1 if successful, 0 if not found)
        """
        try:
            with self.conn:
                # Delete agent (cascading delete will handle signature requests)
                cursor = self.conn.execute("DELETE FROM agent WHERE id = ?", (agent_id,))
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error deleting agent: {e}")
            raise

import sqlite3
from typing import Optional

from heroserver.db import DB
from heroserver.models import JobLog


class ManagerLogs:
    def __init__(self, db: DB):
        self.db = DB

    def add(self, job_id: int, message: str, category: str = "info") -> int:
        """Add a log entry for a job.

        Args:
            job_id: ID of the job
            message: Log message
            category: Log category (default: info)

        Returns:
            int: ID of the created log entry
        """
        try:
            with self.conn:
                # Get the next sequence number for this job
                cursor = self.conn.execute("SELECT COALESCE(MAX(log_sequence), 0) + 1 FROM job_logs WHERE jobid = ?", (job_id,))
                next_sequence = cursor.fetchone()[0]

                # Insert the log entry
                cursor = self.conn.execute(
                    """
                    INSERT INTO job_logs (jobid, log_sequence, message, category)
                    VALUES (?, ?, ?, ?)
                    """,
                    (job_id, next_sequence, message, category),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding log: {e}")
            raise

    def get(self, log_id: int) -> Optional[JobLog]:
        """Get a log entry by ID.

        Args:
            log_id: ID of the log entry to get

        Returns:
            Optional[JobLog]: Log entry if found, None otherwise
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    SELECT * FROM job_logs WHERE id = ?
                    """,
                    (log_id,),
                )
                row = cursor.fetchone()
                if row:
                    return JobLog(
                        id=row["id"],
                        job_id=row["jobid"],
                        log_sequence=row["log_sequence"],
                        message=row["message"],
                        category=row["category"],
                        log_time=row["log_time"],
                    )
                return None
        except sqlite3.Error as e:
            print(f"Error getting log: {e}")
            raise

    def search(self, job_id: int, search_text: str, category: str = None, time_from: int = None, time_to: int = None) -> list[JobLog]:
        """Search logs by message text within a specific job.

        Args:
            job_id: ID of the job to search logs for
            search_text: Text to search for in log messages
            category: Optional category to filter logs by
            time_from: Optional start time (unix timestamp) to filter logs
            time_to: Optional end time (unix timestamp) to filter logs

        Returns:
            list[JobLog]: List of matching log entries

        Raises:
            ValueError: If time range is invalid
        """
        if time_from and time_to and time_from > time_to:
            raise ValueError("time_from must be less than or equal to time_to")

        sql = "SELECT * FROM job_logs WHERE jobid = ? AND message LIKE ?"
        params = [job_id, f"%{search_text}%"]

        if category:
            sql += " AND category = ?"
            params.append(category)

        if time_from is not None:
            sql += " AND log_time >= ?"
            params.append(time_from)

        if time_to is not None:
            sql += " AND log_time <= ?"
            params.append(time_to)

        sql += " ORDER BY log_time DESC"

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                logs = []
                for row in cursor:
                    logs.append(
                        JobLog(
                            id=row["id"],
                            job_id=row["jobid"],
                            log_sequence=row["log_sequence"],
                            message=row["message"],
                            category=row["category"],
                            log_time=row["log_time"],
                        )
                    )
                return logs
        except sqlite3.Error as e:
            print(f"Error searching logs: {e}")
            raise

    def delete(self, job_id: int = None, older_than_seconds: int = None) -> int:
        """Delete logs based on criteria.

        Args:
            job_id: Optional job ID to delete logs for
            older_than_seconds: Optional age in seconds to delete logs older than

        Returns:
            int: Number of logs deleted
        """
        sql = "DELETE FROM job_logs WHERE 1=1"
        params = []

        if job_id:
            sql += " AND jobid = ?"
            params.append(job_id)

        if older_than_seconds:
            sql += " AND log_time < strftime('%s', 'now', ? || ' seconds')"
            params.append(f"-{older_than_seconds}")

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error deleting logs: {e}")
            raise

    def delete_all(self) -> int:
        """Delete all logs from the system.

        Returns:
            int: Number of logs deleted
        """
        try:
            with self.conn:
                cursor = self.conn.execute("DELETE FROM job_logs")
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error deleting all logs: {e}")
            raise

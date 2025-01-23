import sqlite3
from datetime import datetime, timedelta
from typing import Optional

from heroserver.db import DB
from heroserver.models import Job, JobState, JobType


class ManagerJobs:
    def __init__(self, db: DB):
        self.db = DB

    def set(self, job: Job) -> int:
        """Add a job to the queue.

        Args:
            job: Job instance to add

        Returns:
            int: ID of the inserted job
        """
        sql = """
        INSERT INTO job_queue (actor, action, params, job_type, recurring, schedule_date, create_date, deadline, agent_id, signature)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self.conn:
                now = int(datetime.now().timestamp())
                schedule_ts = job.schedule_date if job.schedule_date > 0 else now
                create_ts = job.create_date if job.create_date > 0 else now
                cursor = self.conn.execute(
                    sql,
                    (
                        job.actor,
                        job.action,
                        job.params,
                        job.job_type.value,
                        job.recurring,
                        schedule_ts,
                        create_ts,
                        job.deadline,
                        job.agent_id,
                        job.signature,
                    ),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error setting job: {e}")
            raise

    def queued(self, executor: str = "default", execution_time: int = 300, actor: Optional[str] = None) -> Optional[Job]:
        """Get the next available job and lock it.

        Args:
            execution_time: Time in seconds to lock the job for
            executor: Identifier of who/what is executing the job
            actor: Optional actor name to filter jobs by

        Returns:
            Optional[Job]: Next available job or None if no jobs available
        """
        # First try to get a job that's ready to run
        # Set isolation level to IMMEDIATE to prevent other connections from writing
        self.conn.isolation_level = "IMMEDIATE"

        sql = """
        SELECT * FROM job_queue
        WHERE (locked_until IS NULL OR locked_until < strftime('%s', 'now'))
        AND NOT completed
        AND (schedule_date IS NULL OR schedule_date <= strftime('%s', 'now'))
        AND (deadline IS NULL OR deadline = 0 OR deadline > strftime('%s', 'now'))
        AND (deadline IS NULL OR deadline = 0 OR deadline > strftime('%s', 'now'))
        """

        if actor:
            sql += " AND actor = ?"

        sql += """
        ORDER BY schedule_date, id
        LIMIT 1
        """

        try:
            with self.conn:
                if actor:
                    cursor = self.conn.execute(sql, (actor,))
                else:
                    cursor = self.conn.execute(sql)
                row = cursor.fetchone()

                if row:
                    # Lock the job
                    lock_until = datetime.now() + timedelta(seconds=execution_time)
                    lock_until_ts = int(lock_until.timestamp())
                    self.conn.execute(
                        "UPDATE job_queue SET locked_until = ?, executor = ? WHERE id = ?",
                        (lock_until_ts, executor, row["id"]),
                    )

                    # Get timestamps directly as integers
                    create_date = row["create_date"] or 0
                    schedule_date = row["schedule_date"] or 0
                    finish_date = row["finish_date"] or 0
                    locked_until = row["locked_until"] or 0

                    # Convert row to Job instance with deserialized parameters
                    return Job(
                        id=row["id"],
                        actor=row["actor"],
                        action=row["action"],
                        params=row["params"],
                        job_type=JobType(row["job_type"]),
                        recurring=row["recurring"],
                        state=row["state"],
                        error=row["error"] or "",
                        create_date=create_date,
                        schedule_date=schedule_date,
                        finish_date=finish_date,
                        locked_until=locked_until,
                        completed=bool(row["completed"]),
                        deadline=row["deadline"] or 0,
                        agent_id=row["agent_id"],
                        signature=row["signature"],
                    )
                return None
        except sqlite3.Error as e:
            print(f"Error getting job: {e}")
            raise

    def complete(self, job_id: int, success: bool = True, error: str = ""):
        """Mark a job as completed.

        Args:
            job_id: ID of the job to complete
            success: Whether the job completed successfully
            error: Error message if job failed
        """
        try:
            with self.conn:
                # Mark the job as completed
                self.conn.execute(
                    """
                    UPDATE job_queue 
                    SET completed = 1,
                        state = ?,
                        error = ?,
                        finish_date = strftime('%s', 'now')
                    WHERE id = ?
                    """,
                    (JobState.OK.value if success else JobState.ERROR.value, error, job_id),
                )

                # If job is recurring, create next occurrence
                cursor = self.conn.execute("SELECT * FROM job_queue WHERE id = ?", (job_id,))
                job = cursor.fetchone()

                if job and job["recurring"]:
                    # Schedule next job 24 hours later
                    next_schedule = datetime.now() + timedelta(days=1)
                    next_schedule_ts = int(next_schedule.timestamp())

                    # Insert next occurrence with explicit column values
                    self.conn.execute(
                        """
                        INSERT INTO job_queue 
                        (actor, action, params, job_type, recurring, schedule_date, 
                         completed, state, locked_until, create_date, deadline, agent_id, signature)
                        VALUES (?, ?, ?, ?, ?, ?, 
                               0, ?, NULL, strftime('%s', 'now'), ?, ?, ?)
                        """,
                        (
                            job["actor"],
                            job["action"],
                            job["params"],
                            job["job_type"],
                            job["recurring"],
                            next_schedule_ts,
                            JobState.INIT.value,
                            job["deadline"],
                            job["agent_id"],
                            job["signature"],
                        ),
                    )
        except sqlite3.Error as e:
            print(f"Error completing job: {e}")
            raise

    def waiting(self, actor: Optional[str] = None) -> list[Job]:
        """Get all jobs waiting to be executed.

        Args:
            actor: Optional actor name to filter jobs by

        Returns:
            list[Job]: List of jobs that are not completed and not currently locked
        """
        sql = """
        SELECT * FROM job_queue
        WHERE (locked_until IS NULL OR locked_until < strftime('%s', 'now'))
        AND NOT completed
        AND (schedule_date IS NULL OR schedule_date <= strftime('%s', 'now'))
        """

        if actor:
            sql += " AND actor = ?"

        sql += " ORDER BY schedule_date, id"
        try:
            with self.conn:
                if actor:
                    cursor = self.conn.execute(sql, (actor,))
                else:
                    cursor = self.conn.execute(sql)
                jobs = []
                for row in cursor:
                    # Get timestamps directly as integers
                    create_date = row["create_date"] or 0
                    schedule_date = row["schedule_date"] or 0
                    finish_date = row["finish_date"] or 0
                    locked_until = row["locked_until"] or 0

                    jobs.append(
                        Job(
                            id=row["id"],
                            actor=row["actor"],
                            action=row["action"],
                            params=row["params"],
                            job_type=JobType(row["job_type"]),
                            recurring=row["recurring"],
                            state=row["state"],
                            error=row["error"] or "",
                            create_date=create_date,
                            schedule_date=schedule_date,
                            finish_date=finish_date,
                            locked_until=locked_until,
                            completed=bool(row["completed"]),
                            deadline=row["deadline"] or 0,
                            agent_id=row["agent_id"],
                            signature=row["signature"],
                        )
                    )
                return jobs
        except sqlite3.Error as e:
            print(f"Error getting waiting jobs: {e}")
            raise

    def failed(self, since_seconds: Optional[int] = None, actor: Optional[str] = None) -> list[Job]:
        """Get failed jobs, optionally filtered by time and actor.

        Args:
            since_seconds: If provided, only return jobs that failed within this many seconds ago
            actor: Optional actor name to filter jobs by

        Returns:
            list[Job]: List of failed jobs
        """
        sql = """
        SELECT * FROM job_queue
        WHERE completed = 1 AND state = ?
        """
        params = [JobState.ERROR.value]

        if since_seconds is not None:
            sql += f" AND finish_date >= strftime('%s', 'now', '-{since_seconds} seconds')"

        if actor:
            sql += " AND actor = ?"
            params.append(actor)

        sql += " ORDER BY finish_date DESC"

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                jobs = []
                for row in cursor:
                    # Get timestamps directly as integers
                    create_date = row["create_date"] or 0
                    schedule_date = row["schedule_date"] or 0
                    finish_date = row["finish_date"] or 0
                    locked_until = row["locked_until"] or 0

                    jobs.append(
                        Job(
                            id=row["id"],
                            actor=row["actor"],
                            action=row["action"],
                            params=row["params"],
                            job_type=JobType(row["job_type"]),
                            recurring=row["recurring"],
                            state=row["state"],
                            error=row["error"] or "",
                            create_date=create_date,
                            schedule_date=schedule_date,
                            finish_date=finish_date,
                            locked_until=locked_until,
                            completed=bool(row["completed"]),
                            deadline=row["deadline"] or 0,
                            agent_id=row["agent_id"],
                            signature=row["signature"],
                        )
                    )
                return jobs
        except sqlite3.Error as e:
            print(f"Error getting failed jobs: {e}")
            raise

    def succeeded(self, since_seconds: Optional[int] = None, actor: Optional[str] = None) -> list[Job]:
        """Get succeeded jobs, optionally filtered by time and actor.

        Args:
            since_seconds: If provided, only return jobs that succeeded within this many seconds ago
            actor: Optional actor name to filter jobs by

        Returns:
            list[Job]: List of succeeded jobs
        """
        sql = """
        SELECT * FROM job_queue
        WHERE completed = 1 AND state = ?
        """
        params = [JobState.OK.value]

        if since_seconds is not None:
            sql += f" AND finish_date >= strftime('%s', 'now', '-{since_seconds} seconds')"

        if actor:
            sql += " AND actor = ?"
            params.append(actor)

        sql += " ORDER BY finish_date DESC"

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                jobs = []
                for row in cursor:
                    # Get timestamps directly as integers
                    create_date = row["create_date"] or 0
                    schedule_date = row["schedule_date"] or 0
                    finish_date = row["finish_date"] or 0
                    locked_until = row["locked_until"] or 0

                    jobs.append(
                        Job(
                            id=row["id"],
                            actor=row["actor"],
                            action=row["action"],
                            params=row["params"],
                            job_type=JobType(row["job_type"]),
                            recurring=row["recurring"],
                            state=row["state"],
                            error=row["error"] or "",
                            create_date=create_date,
                            schedule_date=schedule_date,
                            finish_date=finish_date,
                            locked_until=locked_until,
                            completed=bool(row["completed"]),
                            deadline=row["deadline"] or 0,
                            agent_id=row["agent_id"],
                            signature=row["signature"],
                        )
                    )
                return jobs
        except sqlite3.Error as e:
            print(f"Error getting succeeded jobs: {e}")
            raise

    def find(
        self,
        job_type: Optional[JobType] = None,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        state: Optional[JobState] = None,
        create_date_from: Optional[int] = None,
        create_date_to: Optional[int] = None,
        finish_date_from: Optional[int] = None,
        finish_date_to: Optional[int] = None,
        job_id: Optional[int] = None,
        recurring_only: bool = False,
        deadline_from: Optional[int] = None,
        deadline_to: Optional[int] = None,
    ) -> list[Job]:
        """Find jobs based on multiple criteria.

        Args:
            job_type: Filter by job type
            actor: Filter by actor name
            action: Filter by action name
            state: Filter by job state
            create_date_from: Filter by creation date range start (unix timestamp)
            create_date_to: Filter by creation date range end (unix timestamp)
            finish_date_from: Filter by finish date range start (unix timestamp)
            finish_date_to: Filter by finish date range end (unix timestamp)
            job_id: Filter by specific job ID
            recurring_only: If True, only return recurring jobs
            deadline_from: Filter by deadline range start (unix timestamp)
            deadline_to: Filter by deadline range end (unix timestamp)

        Returns:
            list[Job]: List of jobs matching the criteria

        Raises:
            ValueError: If date ranges are invalid
        """
        # Validate date ranges
        if create_date_from and create_date_to and create_date_from > create_date_to:
            raise ValueError("create_date_from must be less than or equal to create_date_to")
        if finish_date_from and finish_date_to and finish_date_from > finish_date_to:
            raise ValueError("finish_date_from must be less than or equal to finish_date_to")
        if deadline_from and deadline_to and deadline_from > deadline_to:
            raise ValueError("deadline_from must be less than or equal to deadline_to")

        sql = "SELECT * FROM job_queue WHERE 1=1"
        params = []

        if job_type:
            if not isinstance(job_type, JobType):
                raise ValueError(f"Invalid job_type: {job_type}")
            sql += " AND job_type = ?"
            params.append(job_type.value)

        if actor:
            sql += " AND actor = ?"
            params.append(actor)

        if action:
            sql += " AND action = ?"
            params.append(action)

        if state:
            if not isinstance(state, JobState):
                raise ValueError(f"Invalid state: {state}")
            sql += " AND state = ?"
            params.append(state.value)

        if create_date_from is not None:
            sql += " AND create_date >= ?"
            params.append(create_date_from)
        if create_date_to is not None:
            sql += " AND create_date <= ?"
            params.append(create_date_to)

        if finish_date_from is not None:
            sql += " AND finish_date >= ?"
            params.append(finish_date_from)
        if finish_date_to is not None:
            sql += " AND finish_date <= ?"
            params.append(finish_date_to)

        if job_id:
            sql += " AND id = ?"
            params.append(job_id)

        if recurring_only:
            sql += " AND recurring != ''"

        if deadline_from is not None:
            sql += " AND deadline >= ?"
            params.append(deadline_from)
        if deadline_to is not None:
            sql += " AND deadline <= ?"
            params.append(deadline_to)

        sql += " ORDER BY create_date DESC"

        try:
            with self.conn:
                cursor = self.conn.execute(sql, params)
                jobs = []
                for row in cursor:
                    # Get timestamps directly as integers
                    create_date = row["create_date"] or 0
                    schedule_date = row["schedule_date"] or 0
                    finish_date = row["finish_date"] or 0
                    locked_until = row["locked_until"] or 0

                    jobs.append(
                        Job(
                            id=row["id"],
                            actor=row["actor"],
                            action=row["action"],
                            params=row["params"],
                            job_type=JobType(row["job_type"]),
                            recurring=row["recurring"],
                            state=row["state"],
                            error=row["error"] or "",
                            create_date=create_date,
                            schedule_date=schedule_date,
                            finish_date=finish_date,
                            locked_until=locked_until,
                            completed=bool(row["completed"]),
                            deadline=row["deadline"] or 0,
                            agent_id=row["agent_id"],
                            signature=row["signature"],
                        )
                    )
                return jobs
        except sqlite3.Error as e:
            print(f"Error finding jobs: {e}")
            raise

    def delete_all(self) -> int:
        """Delete all jobs from the queue.

        Returns:
            int: Number of jobs deleted
        """
        try:
            with self.conn:
                cursor = self.conn.execute("DELETE FROM job_queue")
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error deleting all jobs: {e}")
            raise

    def expire(self, older_than_seconds: int) -> int:
        """Delete completed jobs older than the specified time.

        Args:
            older_than_seconds: Delete completed jobs older than this many seconds

        Returns:
            int: Number of jobs deleted
        """
        sql = """
        DELETE FROM job_queue
        WHERE completed = 1
        AND finish_date < strftime('%s', 'now', ? || ' seconds')
        """
        try:
            with self.conn:
                cursor = self.conn.execute(sql, (f"-{older_than_seconds}",))
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error expiring old jobs: {e}")
            raise

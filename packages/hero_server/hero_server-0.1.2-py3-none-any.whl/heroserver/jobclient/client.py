from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import requests

from heroserver.jobmanager.models import ExecutorState, JobState, JobType


class JobType(Enum):
    """Type of job to execute"""

    HEROSCRIPT = "hero"


@dataclass
class ExecutorResponse:
    """Response object for executor operations"""

    id: int
    name: str
    description: Optional[str]
    state: str


@dataclass
class ActorResponse:
    """Response object for actor operations"""

    id: int
    name: str
    executor_id: int
    description: Optional[str]


@dataclass
class ActionResponse:
    """Response object for action operations"""

    id: int
    name: str
    actor_id: int
    description: Optional[str]
    nrok: int
    nrfailed: int
    code: Optional[str]


@dataclass
class LogEntry:
    """Log entry for a job"""

    id: int
    jobid: int
    log_sequence: int
    message: str
    category: str
    log_time: int


@dataclass
class JobResponse:
    """Response object for job operations"""

    id: int
    actor: str
    action: str
    params: str
    job_type: str
    create_date: int
    schedule_date: int
    finish_date: int
    locked_until: int
    completed: bool
    state: str
    error: str
    recurring: str
    deadline: int


class JobClient:
    """Client for interacting with the Hero Job Queue API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the job client.

        Args:
            base_url: Base URL of the job queue API. Defaults to http://localhost:8000
        """
        self.base_url = base_url.rstrip("/")

    def create_job(
        self,
        actor: str,
        action: str,
        params: str,  # Still accept dict but convert to string
        job_type: JobType = JobType.HEROSCRIPT,
        schedule_date: int = None,
        recurring: str = None,
        deadline: int = 0,
    ) -> JobResponse:
        """Create a new job in the queue.

        Args:
            actor: The actor that will execute this job
            action: The action to be performed
            params: Optional parameters for the job
            job_type: Optional type of the job
            schedule_date: Optional timestamp for when to schedule the job
            recurring: Optional recurring schedule specification
            deadline: Optional unix timestamp for job deadline (default: 0)

        Returns:
            JobResponse object containing the created job details

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "actor": actor,
            "action": action,
            "params": params,
            "job_type": job_type.value if isinstance(job_type, JobType) else JobType.HEROSCRIPT.value,
            "schedule_date": schedule_date if schedule_date is not None else 0,
            "recurring": recurring if recurring is not None else "",
            "deadline": deadline,
        }
        try:
            response = requests.post(f"{self.base_url}/jobs", json=data)
            response.raise_for_status()
            return JobResponse(**response.json())
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                    raise requests.exceptions.HTTPError(f"Server error: {error_detail.get('detail', str(e))}") from e
                except ValueError:
                    pass
            raise

    def get_next_job(self) -> Optional[JobResponse]:
        """Get and lock the next available job from the queue.

        Returns:
            JobResponse object if a job is available, None otherwise

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.get(f"{self.base_url}/jobs/queued")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return JobResponse(**response.json())

    def get_waiting_jobs(self, actor: Optional[str] = None) -> List[JobResponse]:
        """Get all jobs waiting to be executed.

        Args:
            actor: Optional actor name to filter jobs

        Returns:
            List of JobResponse objects representing waiting jobs

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {"actor": actor} if actor else {}
        response = requests.get(f"{self.base_url}/jobs/waiting", params=params)
        response.raise_for_status()
        return [JobResponse(**job) for job in response.json()]

    def get_failed_jobs(self, since_seconds: Optional[int] = None, actor: Optional[str] = None) -> List[JobResponse]:
        """Get failed jobs, optionally filtered by time and actor.

        Args:
            since_seconds: Optional number of seconds to look back
            actor: Optional actor name to filter jobs

        Returns:
            List of JobResponse objects representing failed jobs

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {}
        if since_seconds is not None:
            params["since_seconds"] = since_seconds
        if actor:
            params["actor"] = actor
        response = requests.get(f"{self.base_url}/jobs/failed", params=params)
        response.raise_for_status()
        return [JobResponse(**job) for job in response.json()]

    def get_succeeded_jobs(self, since_seconds: Optional[int] = None, actor: Optional[str] = None) -> List[JobResponse]:
        """Get succeeded jobs, optionally filtered by time and actor.

        Args:
            since_seconds: Optional number of seconds to look back
            actor: Optional actor name to filter jobs

        Returns:
            List of JobResponse objects representing succeeded jobs

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {}
        if since_seconds is not None:
            params["since_seconds"] = since_seconds
        if actor:
            params["actor"] = actor
        response = requests.get(f"{self.base_url}/jobs/succeeded", params=params)
        response.raise_for_status()
        return [JobResponse(**job) for job in response.json()]

    def complete_job(self, job_id: int, success: bool, error: str = "") -> None:
        """Mark a job as completed.

        Args:
            job_id: ID of the job to complete
            success: Whether the job completed successfully
            error: Optional error message if the job failed

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {"success": success, "error": error}
        response = requests.post(f"{self.base_url}/jobs/{job_id}/complete", json=data)
        response.raise_for_status()

    def add_log(self, job_id: int, message: str, category: str = "info") -> int:
        """Add a log entry for a job.

        Args:
            job_id: ID of the job to add log for
            message: Log message
            category: Optional log category (default: "info")

        Returns:
            ID of the created log entry

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {"message": message, "category": category}
        response = requests.post(f"{self.base_url}/jobs/{job_id}/logs", params=params)
        response.raise_for_status()
        return response.json()["log_id"]

    def get_logs(
        self, job_id: int, category: Optional[str] = None, time_from: Optional[int] = None, time_to: Optional[int] = None
    ) -> List[LogEntry]:
        """Get logs for a specific job.

        Args:
            job_id: ID of the job to get logs for
            category: Optional category to filter logs
            time_from: Optional start time (unix timestamp) to filter logs
            time_to: Optional end time (unix timestamp) to filter logs

        Returns:
            List of LogEntry objects

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {}
        if category:
            params["category"] = category
        if time_from is not None:
            params["time_from"] = time_from
        if time_to is not None:
            params["time_to"] = time_to
        response = requests.get(f"{self.base_url}/jobs/{job_id}/logs", params=params)
        response.raise_for_status()
        return [LogEntry(**log) for log in response.json()]

    def delete_logs(self, job_id: Optional[int] = None, older_than_seconds: Optional[int] = None) -> int:
        """Delete logs based on criteria.

        Args:
            job_id: Optional job ID to delete logs for
            older_than_seconds: Optional time threshold in seconds

        Returns:
            Number of deleted log entries

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {}
        if job_id:
            params["job_id"] = job_id
        if older_than_seconds is not None:
            params["older_than_seconds"] = older_than_seconds
        response = requests.delete(f"{self.base_url}/logs", params=params)
        response.raise_for_status()
        return response.json()["deleted_count"]

    def fail_deadline_jobs(self) -> int:
        """Mark jobs as failed if they are past their deadline.

        Returns:
            Number of jobs marked as failed

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.post(f"{self.base_url}/jobs/fail-deadline")
        response.raise_for_status()
        return response.json()["failed_count"]

    def find_jobs(
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
    ) -> List[JobResponse]:
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
            List[JobResponse]: List of jobs matching the criteria

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {}
        if job_type:
            if not isinstance(job_type, JobType):
                raise ValueError(f"Invalid job_type: {job_type}")
            params["job_type"] = job_type.value
        if actor:
            params["actor"] = actor
        if action:
            params["action"] = action
        if state:
            if not isinstance(state, JobState):
                raise ValueError(f"Invalid state: {state}")
            params["state"] = state.value
        if create_date_from is not None:
            params["create_date_from"] = create_date_from
        if create_date_to is not None:
            params["create_date_to"] = create_date_to
        if finish_date_from is not None:
            params["finish_date_from"] = finish_date_from
        if finish_date_to is not None:
            params["finish_date_to"] = finish_date_to
        if job_id:
            params["job_id"] = job_id
        if recurring_only:
            params["recurring_only"] = recurring_only
        if deadline_from is not None:
            params["deadline_from"] = deadline_from
        if deadline_to is not None:
            params["deadline_to"] = deadline_to

        try:
            response = requests.get(f"{self.base_url}/jobs/find", params=params)
            response.raise_for_status()
            return [JobResponse(**job) for job in response.json()]
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                    raise requests.exceptions.HTTPError(f"Server error: {error_detail.get('detail', str(e))}") from e
                except ValueError:
                    pass
            raise

    def delete_all_jobs(self) -> int:
        """Delete all jobs from the queue.

        Returns:
            int: Number of jobs deleted

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.delete(f"{self.base_url}/jobs/all")
        response.raise_for_status()
        return response.json()["deleted_count"]

    def delete_all_logs(self) -> int:
        """Delete all logs from the system.

        Returns:
            int: Number of logs deleted

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.delete(f"{self.base_url}/logs/all")
        response.raise_for_status()
        return response.json()["deleted_count"]

    # Executor operations
    def create_executor(self, name: str, description: Optional[str] = None, state: ExecutorState = ExecutorState.INIT) -> ExecutorResponse:
        """Create a new executor.

        Args:
            name: Name of the executor
            description: Optional description
            state: Initial state (default: INIT)

        Returns:
            ExecutorResponse object containing the created executor details

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {"name": name, "description": description, "state": state.value}
        response = requests.post(f"{self.base_url}/executors", json=data)
        response.raise_for_status()
        return ExecutorResponse(**response.json())

    def get_executor(self, executor_id: int) -> ExecutorResponse:
        """Get an executor by ID.

        Args:
            executor_id: ID of the executor to retrieve

        Returns:
            ExecutorResponse object containing the executor details

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.get(f"{self.base_url}/executors/{executor_id}")
        response.raise_for_status()
        return ExecutorResponse(**response.json())

    def list_executors(self) -> List[ExecutorResponse]:
        """List all executors.

        Returns:
            List of ExecutorResponse objects

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.get(f"{self.base_url}/executors")
        response.raise_for_status()
        return [ExecutorResponse(**executor) for executor in response.json()]

    # Actor operations
    def create_actor(self, name: str, executor_id: int, description: Optional[str] = None) -> ActorResponse:
        """Create a new actor.

        Args:
            name: Name of the actor
            executor_id: ID of the associated executor
            description: Optional description

        Returns:
            ActorResponse object containing the created actor details

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {"name": name, "executor_id": executor_id, "description": description}
        response = requests.post(f"{self.base_url}/actors", json=data)
        response.raise_for_status()
        return ActorResponse(**response.json())

    def get_actor(self, actor_id: int) -> ActorResponse:
        """Get an actor by ID.

        Args:
            actor_id: ID of the actor to retrieve

        Returns:
            ActorResponse object containing the actor details

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.get(f"{self.base_url}/actors/{actor_id}")
        response.raise_for_status()
        return ActorResponse(**response.json())

    def list_actors(self, executor_id: Optional[int] = None) -> List[ActorResponse]:
        """List actors, optionally filtered by executor_id.

        Args:
            executor_id: Optional ID of executor to filter by

        Returns:
            List of ActorResponse objects

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {"executor_id": executor_id} if executor_id else {}
        response = requests.get(f"{self.base_url}/actors", params=params)
        response.raise_for_status()
        return [ActorResponse(**actor) for actor in response.json()]

    # Action operations
    def create_action(self, name: str, actor_id: int, description: Optional[str] = None, code: Optional[str] = None) -> ActionResponse:
        """Create a new action.

        Args:
            name: Name of the action
            actor_id: ID of the associated actor
            description: Optional description
            code: Optional code for the action

        Returns:
            ActionResponse object containing the created action details

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {"name": name, "actor_id": actor_id, "description": description, "code": code}
        response = requests.post(f"{self.base_url}/actions", json=data)
        response.raise_for_status()
        return ActionResponse(**response.json())

    def get_action(self, action_id: int) -> ActionResponse:
        """Get an action by ID.

        Args:
            action_id: ID of the action to retrieve

        Returns:
            ActionResponse object containing the action details

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.get(f"{self.base_url}/actions/{action_id}")
        response.raise_for_status()
        return ActionResponse(**response.json())

    def list_actions(self, actor_id: Optional[int] = None) -> List[ActionResponse]:
        """List actions, optionally filtered by actor_id.

        Args:
            actor_id: Optional ID of actor to filter by

        Returns:
            List of ActionResponse objects

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        params = {"actor_id": actor_id} if actor_id else {}
        response = requests.get(f"{self.base_url}/actions", params=params)
        response.raise_for_status()
        return [ActionResponse(**action) for action in response.json()]

    # Delete operations
    def delete_executor(self, executor_id: int) -> int:
        """Delete an executor and all its associated actors and actions.

        Args:
            executor_id: ID of the executor to delete

        Returns:
            Number of executors deleted (1 if successful, 0 if not found)

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.delete(f"{self.base_url}/executors/{executor_id}")
        response.raise_for_status()
        return response.json()["deleted_count"]

    def delete_actor(self, actor_id: int) -> int:
        """Delete an actor and all its associated actions.

        Args:
            actor_id: ID of the actor to delete

        Returns:
            Number of actors deleted (1 if successful, 0 if not found)

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.delete(f"{self.base_url}/actors/{actor_id}")
        response.raise_for_status()
        return response.json()["deleted_count"]

    def delete_action(self, action_id: int) -> int:
        """Delete an action.

        Args:
            action_id: ID of the action to delete

        Returns:
            Number of actions deleted (1 if successful, 0 if not found)

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.delete(f"{self.base_url}/actions/{action_id}")
        response.raise_for_status()
        return response.json()["deleted_count"]

    def expire_jobs(self, older_than_seconds: int) -> int:
        """Delete completed jobs older than the specified time.

        Args:
            older_than_seconds: Time threshold in seconds

        Returns:
            Number of deleted jobs

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = requests.delete(f"{self.base_url}/jobs/expired", params={"older_than_seconds": older_than_seconds})
        response.raise_for_status()
        return response.json()["deleted_count"]

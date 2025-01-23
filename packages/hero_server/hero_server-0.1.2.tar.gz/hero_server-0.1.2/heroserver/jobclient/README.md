# Hero Job Queue Client

A Python client for interacting with the Hero Job Queue API.

## Installation

This client is part of the hero_server_python package. Make sure you have the required dependencies installed:

```bash
pip install requests
```

## Usage

```python
from jobclient import JobClient

# Initialize the client
client = JobClient(base_url="http://localhost:8000")  # Default URL

# Create a new job
job = client.create_job(
    actor="my_actor",
    action="process_data",
    params={"data_id": "123"},  # optional
    job_type=JobType.HEROSCRIPT,  # optional, defaults to JobType.HEROSCRIPT
    schedule_date=1234567890,   # optional, unix timestamp (default: 0)
    recurring="0 0 * * *",      # optional, cron expression (default: "")
    deadline=1234567890         # optional, unix timestamp for deadline
)

# Get the next available job
next_job = client.get_next_job()
if next_job:
    print(f"Got job: {next_job.id}")

# Get all waiting jobs
waiting_jobs = client.get_waiting_jobs(actor="my_actor")  # actor filter is optional
for job in waiting_jobs:
    print(f"Waiting job: {job.id}")

# Get failed jobs from the last hour
failed_jobs = client.get_failed_jobs(
    since_seconds=3600,  # optional
    actor="my_actor"     # optional
)

# Get succeeded jobs
succeeded_jobs = client.get_succeeded_jobs(
    since_seconds=3600,  # optional
    actor="my_actor"     # optional
)
```

## API Reference

### JobClient

#### `__init__(base_url: str = "http://localhost:8000")`
Initialize the job client with the API base URL.

#### `create_job(actor: str, action: str, params: Optional[dict] = None, job_type: JobType = JobType.HEROSCRIPT, schedule_date: Optional[int] = 0, recurring: str = "", deadline: int = 0) -> JobResponse`
Create a new job in the queue. The actor and action are required, while other parameters are optional.

#### `get_next_job() -> Optional[JobResponse]`
Get and lock the next available job from the queue.

#### `get_waiting_jobs(actor: Optional[str] = None) -> List[JobResponse]`
Get all jobs waiting to be executed.

#### `get_failed_jobs(since_seconds: Optional[int] = None, actor: Optional[str] = None) -> List[JobResponse]`
Get failed jobs, optionally filtered by time and actor.

#### `get_succeeded_jobs(since_seconds: Optional[int] = None, actor: Optional[str] = None) -> List[JobResponse]`
Get succeeded jobs, optionally filtered by time and actor.

### LogEntry

A dataclass representing a log entry with the following fields:
- `id: int` - The log entry ID
- `jobid: int` - ID of the associated job
- `log_sequence: int` - Sequence number of the log entry
- `message: str` - The log message
- `category: str` - Category of the log entry
- `log_time: int` - Unix timestamp when the log was created

### JobResponse

A dataclass representing a job response from the API with the following fields:
- `id: str` - The job ID
- `actor: str` - The actor that will execute this job
- `action: str` - The action to be performed
- `params: dict` - Parameters for the job
- `job_type: str` - Type of the job
- `create_date: int` - Unix timestamp when the job was created
- `schedule_date: int` - Unix timestamp when the job is scheduled to run
- `finish_date: int` - Unix timestamp when the job finished
- `locked_until: int` - Unix timestamp until when the job is locked
- `completed: bool` - Whether the job is completed
- `state: str` - Current state of the job
- `error: str` - Error message if the job failed
- `recurring: str` - Recurring schedule specification (cron expression)
- `deadline: int` - Unix timestamp for job deadline

### JobType

An enum representing the type of job:
- `HEROSCRIPT = "hero"` - Default job type for hero scripts

## Error Handling

All methods may raise `requests.exceptions.RequestException` if the API request fails. For HTTP errors, the client will attempt to extract and display the detailed error message from the server. Handle these exceptions appropriately in your code:

```python
from requests.exceptions import RequestException

try:
    job = client.create_job(
        actor="my_actor",
        action="process_data",
        params={"data_id": "123"}
    )
except RequestException as e:
    print(f"API request failed: {e}")  # Will include server's error details if available
```

## Job Management

```python
# Complete a job
client.complete_job(job_id="123", success=True)
# Or with error if failed
client.complete_job(job_id="123", success=False, error="Processing failed")

# Mark jobs as failed if past deadline
failed_count = client.fail_deadline_jobs()
print(f"Failed {failed_count} jobs due to deadline")

# Delete old completed jobs
deleted_count = client.expire_jobs(older_than_seconds=86400)  # 24 hours
print(f"Deleted {deleted_count} old jobs")

# Find jobs with various filters
jobs = client.find_jobs(
    actor="my_actor",                    # Filter by actor
    state=JobState.ERROR,                # Filter by state
    job_type=JobType.HEROSCRIPT,        # Filter by job type
    create_date_from=1234567890,        # Filter by creation date range
    create_date_to=1234567899,
    recurring_only=True,                 # Only show recurring jobs
    deadline_from=1234567890,           # Filter by deadline range
    deadline_to=1234567899
)
print(f"Found {len(jobs)} matching jobs")
```

## Job Search

The `find_jobs` method allows searching for jobs with multiple criteria:

```python
from heroserver.jobmanager.models import JobState, JobType

# Find all failed jobs for a specific actor
failed_jobs = client.find_jobs(
    actor="my_actor",
    state=JobState.ERROR
)

# Find recurring jobs with upcoming deadlines
upcoming_jobs = client.find_jobs(
    recurring_only=True,
    deadline_from=int(time.time())  # From now onwards
)

# Find jobs created in a date range
jobs = client.find_jobs(
    create_date_from=1234567890,
    create_date_to=1234567899,
    job_type=JobType.HEROSCRIPT
)
```

Available search criteria:
- `job_type`: Filter by JobType enum (HEROSCRIPT)
- `actor`: Filter by actor name
- `action`: Filter by action name
- `state`: Filter by JobState enum (INIT, STARTED, ERROR, OK, ABORTED)
- `create_date_from/to`: Filter by creation date range (unix timestamps)
- `finish_date_from/to`: Filter by finish date range (unix timestamps)
- `job_id`: Filter by specific job ID
- `recurring_only`: Only show recurring jobs
- `deadline_from/to`: Filter by deadline range (unix timestamps)

## Log Management

```python
# Add a log entry
log_id = client.add_log(
    job_id="123",
    message="Processing started",
    category="info"  # optional, defaults to "info"
)

# Get logs for a job
logs = client.get_logs(job_id="123")
# Or filter by category
logs = client.get_logs(job_id="123", category="error")

# Search logs
logs = client.search_logs(search_text="error occurred")
# Or search with category filter
logs = client.search_logs(search_text="error occurred", category="error")

# Delete old logs
deleted_count = client.delete_logs(older_than_seconds=86400)  # 24 hours
# Or delete logs for specific job
deleted_count = client.delete_logs(job_id="123")
```

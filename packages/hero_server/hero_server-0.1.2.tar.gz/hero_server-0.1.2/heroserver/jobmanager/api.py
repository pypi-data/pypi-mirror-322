from enum import Enum
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, validator

from heroserver.db import DB
from heroserver.jobmanager.manager_actions import ManagerActions
from heroserver.jobmanager.manager_actors import ManagerActors
from heroserver.jobmanager.manager_agents import ManagerAgents
from heroserver.jobmanager.manager_executors import ManagerExecutors
from heroserver.jobmanager.manager_jobs import ManagerJobs
from heroserver.jobmanager.manager_logs import ManagerLogs
from heroserver.jobmanager.manager_signing import ManagerSigning
from heroserver.jobmanager.models import Action, Actor, Agent, Executor, ExecutorState, Job, JobState, JobType, SignatureRequest

app = FastAPI(
    title="Hero Job Queue API",
    description="API for managing the Hero job queue system",
    version="1.0.0",
)

# Initialize database connection
db = DB()

# Initialize managers
job_manager = ManagerJobs(db)
actor_manager = ManagerActors(db)
action_manager = ManagerActions(db)
agent_manager = ManagerAgents(db)
executor_manager = ManagerExecutors(db)
log_manager = ManagerLogs(db)
signing_manager = ManagerSigning(db)


# Pydantic models for request/response validation
class ExecutorStateEnum(str, Enum):
    """Enum for executor states that matches ExecutorState"""

    INIT = "init"
    RUNNING = "running"
    ERROR = "error"
    HALTED = "halted"


class JobTypeEnum(str, Enum):
    """Enum for job types that matches JobType"""

    HEROSCRIPT = "hero"


class SignatureRequestCreate(BaseModel):
    pubkey: str
    signature: str
    verified: bool = False

    @validator("pubkey")
    def pubkey_not_empty(cls, v):
        if not v.strip():
            raise ValueError("pubkey cannot be empty")
        return v

    @validator("signature")
    def signature_not_empty(cls, v):
        if not v.strip():
            raise ValueError("signature cannot be empty")
        return v


class SignatureRequestResponse(BaseModel):
    id: int
    pubkey: str
    signature: str
    date: int
    verified: bool


class AgentCreate(BaseModel):
    name: str
    description: str
    ipaddr: str
    pubkey: str
    location: str

    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v

    @validator("pubkey")
    def pubkey_not_empty(cls, v):
        if not v.strip():
            raise ValueError("pubkey cannot be empty")
        return v


class AgentResponse(BaseModel):
    id: int
    name: str
    description: str
    ipaddr: str
    pubkey: str
    location: str
    signatures: List[SignatureRequestResponse]
    create_date: int


class JobParams(BaseModel):
    actor: str
    action: str
    params: str
    job_type: JobTypeEnum = JobTypeEnum.HEROSCRIPT
    schedule_date: int = 0
    recurring: str = ""
    deadline: int = 0
    agent_id: Optional[int] = None
    signature: Optional[str] = None

    @validator("actor")
    def actor_not_empty(cls, v):
        if not v.strip():
            raise ValueError("actor cannot be empty")
        return v

    @validator("action")
    def action_not_empty(cls, v):
        if not v.strip():
            raise ValueError("action cannot be empty")
        return v

    @validator("schedule_date")
    def schedule_date_not_negative(cls, v):
        if v < 0:
            raise ValueError("schedule_date cannot be negative")
        return v

    @validator("deadline")
    def deadline_not_negative(cls, v):
        if v < 0:
            raise ValueError("deadline cannot be negative")
        return v


class JobResponse(BaseModel):
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
    agent_id: Optional[int]
    signature: Optional[str]


class ExecutorCreate(BaseModel):
    name: str
    description: Optional[str] = None
    state: ExecutorStateEnum = ExecutorStateEnum.INIT

    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v


class ExecutorResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    state: str


class ActorCreate(BaseModel):
    name: str
    executor_id: int
    description: Optional[str] = None

    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v


class ActorResponse(BaseModel):
    id: int
    name: str
    executor_id: int
    description: Optional[str]


class ActionCreate(BaseModel):
    name: str
    actor_id: int
    description: Optional[str] = None
    code: Optional[str] = None

    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v


class ActionResponse(BaseModel):
    id: int
    name: str
    actor_id: int
    description: Optional[str]
    nrok: int
    nrfailed: int
    code: Optional[str]


class CompleteJobRequest(BaseModel):
    success: bool
    error: str = ""


class LogEntry(BaseModel):
    id: int
    jobid: int
    log_sequence: int
    message: str
    category: str
    log_time: int


def job_to_response(job: Job) -> JobResponse:
    """Convert Job instance to JobResponse model"""
    return JobResponse(
        id=int(job.id),
        actor=job.actor,
        action=job.action,
        params=job.params,
        job_type=job.job_type.value,
        create_date=job.create_date,
        schedule_date=job.schedule_date,
        finish_date=job.finish_date,
        locked_until=job.locked_until,
        completed=job.completed,
        state=job.state,
        error=job.error,
        recurring=job.recurring,
        deadline=job.deadline,
        agent_id=job.agent_id,
        signature=job.signature,
    )


# Agent endpoints
@app.post("/agents", response_model=AgentResponse, tags=["agents"])
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    try:
        agent_obj = Agent(
            name=agent.name,
            description=agent.description,
            ipaddr=agent.ipaddr,
            pubkey=agent.pubkey,
            location=agent.location,
        )
        agent_id = agent_manager.add(
            name=agent.name, description=agent.description, ipaddr=agent.ipaddr, pubkey=agent.pubkey, location=agent.location
        )
        return agent_manager.get(agent_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/agents/{agent_id}", response_model=AgentResponse, tags=["agents"])
async def get_agent(agent_id: int):
    """Get an agent by ID"""
    try:
        agent = agent_manager.get(agent_id)
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        return agent
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/agents", response_model=List[AgentResponse], tags=["agents"])
async def list_agents():
    """List all agents"""
    try:
        return agent_manager.list()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/agents/{agent_id}/signatures", response_model=SignatureRequestResponse, tags=["agents"])
async def add_signature_request(agent_id: int, signature_request: SignatureRequestCreate):
    """Add a signature request to an agent"""
    try:
        sig_req = SignatureRequest(
            pubkey=signature_request.pubkey,
            signature=signature_request.signature,
            verified=signature_request.verified,
        )
        sig_id = signing_manager.add(agent_id, sig_req.pubkey, sig_req.signature, sig_req.verified)
        return signing_manager.get(sig_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/agents/{agent_id}/signatures", response_model=List[SignatureRequestResponse], tags=["agents"])
async def get_signature_requests(agent_id: int):
    """Get all signature requests for an agent"""
    try:
        return signing_manager.list(agent_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/agents/{agent_id}", response_model=Dict[str, int], tags=["agents"])
async def delete_agent(agent_id: int):
    """Delete an agent and all its associated signature requests"""
    try:
        deleted_count = agent_manager.delete(agent_id)
        return {"deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Job endpoints
@app.post("/jobs", response_model=JobResponse, tags=["jobs"])
async def create_job(job_params: JobParams):
    """Create a new job in the queue"""
    job = Job(
        actor=job_params.actor,
        action=job_params.action,
        params=job_params.params,
        job_type=JobType(job_params.job_type),
        schedule_date=job_params.schedule_date,
        recurring=job_params.recurring,
        deadline=job_params.deadline,
        agent_id=job_params.agent_id,
        signature=job_params.signature,
    )

    try:
        job_id = job_manager.add(job)
        return job_to_response(job_manager.get(job_id))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid job parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create job: {str(e)}")


@app.get("/jobs/queued", response_model=Optional[JobResponse], tags=["jobs"])
async def get_queued_job(executor: str = "default", execution_time: int = 300, actor: Optional[str] = None):
    """Get the next available job and lock it"""
    try:
        job = job_manager.queued(executor, execution_time, actor)
        if job:
            return job_to_response(job)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get queued job: {str(e)}")


@app.get("/jobs/waiting", response_model=List[JobResponse], tags=["jobs"])
async def get_waiting_jobs(actor: Optional[str] = None):
    """Get all jobs waiting to be executed"""
    try:
        jobs = job_manager.waiting(actor)
        return [job_to_response(job) for job in jobs]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get waiting jobs: {str(e)}")


@app.get("/jobs/failed", response_model=List[JobResponse], tags=["jobs"])
async def get_failed_jobs(since_seconds: Optional[int] = None, actor: Optional[str] = None):
    """Get failed jobs, optionally filtered by time and actor"""
    try:
        jobs = job_manager.failed(since_seconds, actor)
        return [job_to_response(job) for job in jobs]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get failed jobs: {str(e)}")


@app.get("/jobs/succeeded", response_model=List[JobResponse], tags=["jobs"])
async def get_succeeded_jobs(since_seconds: Optional[int] = None, actor: Optional[str] = None):
    """Get succeeded jobs, optionally filtered by time and actor"""
    try:
        jobs = job_manager.succeeded(since_seconds, actor)
        return [job_to_response(job) for job in jobs]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get succeeded jobs: {str(e)}")


@app.post("/jobs/{job_id}/complete", response_model=None, tags=["jobs"])
async def complete_job(job_id: int, complete_request: CompleteJobRequest):
    """Mark a job as completed"""
    try:
        job_manager.complete(job_id, complete_request.success, complete_request.error)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to complete job: {str(e)}")


# Log endpoints
@app.post("/jobs/{job_id}/logs", response_model=Dict[str, int], tags=["logs"])
async def add_log(
    job_id: int, message: str = Query(..., description="Log message"), category: str = Query("info", description="Log category")
):
    """Add a log entry for a job"""
    try:
        log_id = log_manager.add(job_id, message, category)
        return {"log_id": log_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to add log: {str(e)}")


@app.get("/jobs/{job_id}/logs", response_model=List[LogEntry], tags=["logs"])
async def get_logs(
    job_id: int,
    category: Optional[str] = Query(None, description="Optional category to filter logs by"),
    time_from: Optional[int] = Query(None, description="Start time (unix timestamp) to filter logs"),
    time_to: Optional[int] = Query(None, description="End time (unix timestamp) to filter logs"),
    search_text: Optional[str] = Query(None, description="Optional text to search for in log messages"),
):
    """Get logs for a specific job with optional filtering"""
    try:
        if search_text:
            logs = log_manager.search(job_id, search_text, category, time_from, time_to)
        else:
            logs = log_manager.get(job_id)
        return logs
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get logs: {str(e)}")


@app.delete("/logs", response_model=Dict[str, int], tags=["logs"])
async def delete_logs(job_id: Optional[int] = None, older_than_seconds: Optional[int] = None):
    """Delete logs based on criteria"""
    try:
        deleted_count = log_manager.delete(job_id, older_than_seconds)
        return {"deleted_count": deleted_count}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete logs: {str(e)}")


@app.post("/jobs/fail-deadline", response_model=Dict[str, int], tags=["jobs"])
async def fail_deadline_jobs():
    """Mark jobs as failed if they are past their deadline"""
    try:
        failed_count = job_manager.fail_deadline()
        return {"failed_count": failed_count}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fail deadline jobs: {str(e)}")


@app.get("/jobs/find", response_model=List[JobResponse], tags=["jobs"])
async def find_jobs(
    job_type: Optional[str] = None,
    actor: Optional[str] = None,
    action: Optional[str] = None,
    state: Optional[str] = None,
    create_date_from: Optional[int] = None,
    create_date_to: Optional[int] = None,
    finish_date_from: Optional[int] = None,
    finish_date_to: Optional[int] = None,
    job_id: Optional[int] = None,
    recurring_only: bool = False,
    deadline_from: Optional[int] = None,
    deadline_to: Optional[int] = None,
):
    """Find jobs based on multiple criteria"""
    try:
        job_type_enum = JobType(job_type) if job_type else None
        state_enum = JobState(state) if state else None

        jobs = job_manager.find(
            job_type=job_type_enum,
            actor=actor,
            action=action,
            state=state_enum,
            create_date_from=create_date_from,
            create_date_to=create_date_to,
            finish_date_from=finish_date_from,
            finish_date_to=finish_date_to,
            job_id=job_id,
            recurring_only=recurring_only,
            deadline_from=deadline_from,
            deadline_to=deadline_to,
        )
        return [job_to_response(job) for job in jobs]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to find jobs: {str(e)}")


@app.delete("/jobs/all", response_model=Dict[str, int], tags=["jobs"])
async def delete_all_jobs():
    """Delete all jobs from the queue"""
    try:
        deleted_count = job_manager.delete_all()
        return {"deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete all jobs: {str(e)}")


@app.delete("/logs/all", response_model=Dict[str, int], tags=["logs"])
async def delete_all_logs():
    """Delete all logs from the system"""
    try:
        deleted_count = log_manager.delete_all()
        return {"deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete all logs: {str(e)}")


@app.delete("/jobs/expired", tags=["jobs"])
async def expire_jobs(older_than_seconds: int):
    """Delete completed jobs older than the specified time"""
    try:
        deleted_count = job_manager.expire(older_than_seconds)
        return {"deleted_count": deleted_count}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to expire jobs: {str(e)}")


# Executor endpoints
@app.post("/executors", response_model=ExecutorResponse, tags=["executors"])
async def create_executor(executor: ExecutorCreate):
    """Create a new executor"""
    try:
        executor_obj = Executor(name=executor.name, description=executor.description, state=ExecutorState(executor.state))
        executor_id = executor_manager.add(name=executor.name, description=executor.description, state=ExecutorState(executor.state))
        return executor_manager.get(executor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/executors/{executor_id}", response_model=ExecutorResponse, tags=["executors"])
async def get_executor(executor_id: int):
    """Get an executor by ID"""
    try:
        executor = executor_manager.get(executor_id)
        if not executor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Executor not found")
        return executor
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/executors", response_model=List[ExecutorResponse], tags=["executors"])
async def list_executors():
    """List all executors"""
    try:
        return executor_manager.list()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Actor endpoints
@app.post("/actors", response_model=ActorResponse, tags=["actors"])
async def create_actor(actor: ActorCreate):
    """Create a new actor"""
    try:
        actor_obj = Actor(name=actor.name, executor_id=actor.executor_id, description=actor.description)
        actor_id = actor_manager.add(name=actor.name, executor=executor_manager.get(actor.executor_id), description=actor.description)
        return actor_manager.get(actor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/actors/{actor_id}", response_model=ActorResponse, tags=["actors"])
async def get_actor(actor_id: int):
    """Get an actor by ID"""
    try:
        actor = actor_manager.get(actor_id)
        if not actor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found")
        return actor
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/actors", response_model=List[ActorResponse], tags=["actors"])
async def list_actors(executor_id: Optional[int] = None):
    """List all actors, optionally filtered by executor_id"""
    try:
        return actor_manager.list(executor_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Action endpoints
@app.post("/actions", response_model=ActionResponse, tags=["actions"])
async def create_action(action: ActionCreate):
    """Create a new action"""
    try:
        action_obj = Action(name=action.name, actor_id=action.actor_id, description=action.description, code=action.code)
        action_id = action_manager.add(
            name=action.name, actor=actor_manager.get(action.actor_id), description=action.description, code=action.code
        )
        return action_manager.get(action_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/actions/{action_id}", response_model=ActionResponse, tags=["actions"])
async def get_action(action_id: int):
    """Get an action by ID"""
    try:
        action = action_manager.get(action_id)
        if not action:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found")
        return action
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/actions", response_model=List[ActionResponse], tags=["actions"])
async def list_actions(actor_id: Optional[int] = None):
    """List all actions, optionally filtered by actor_id"""
    try:
        return action_manager.list(actor_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Delete endpoints
@app.delete("/executors/{executor_id}", response_model=Dict[str, int], tags=["executors"])
async def delete_executor(executor_id: int):
    """Delete an executor and all its associated actors and actions"""
    try:
        deleted_count = executor_manager.delete(executor_id)
        return {"deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/actors/{actor_id}", response_model=Dict[str, int], tags=["actors"])
async def delete_actor(actor_id: int):
    """Delete an actor and all its associated actions"""
    try:
        deleted_count = actor_manager.delete(actor_id)
        return {"deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/actions/{action_id}", response_model=Dict[str, int], tags=["actions"])
async def delete_action(action_id: int):
    """Delete an action"""
    try:
        deleted_count = action_manager.delete(action_id)
        return {"deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

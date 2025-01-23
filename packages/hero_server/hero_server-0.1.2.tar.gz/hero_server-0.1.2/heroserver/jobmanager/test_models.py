import datetime

from models import Action, Actor, Agent, Executor, Job, JobLog, SignatureRequest, database
from peewee import *

# Initialize SQLite database for testing
test_db = SqliteDatabase(":memory:")
database.initialize(test_db)


def setup_database():
    """Create tables and test data"""
    # Create tables
    test_db.create_tables([Agent, Executor, Actor, Action, Job, SignatureRequest, JobLog])


def test_agent():
    print("\n=== Testing Agent Model ===")

    # Create
    agent1 = Agent.create(name="agent1", description="Test agent 1", ipaddr="192.168.1.1", pubkey="ssh-rsa AAAA...", location="NYC")
    agent2 = Agent.create(name="agent2", description="Test agent 2", ipaddr="192.168.1.2", pubkey="ssh-rsa BBBB...", location="LA")

    # Read/Search
    print("All agents:")
    for agent in Agent.select():
        print(f"- {agent.name}: {agent.description} ({agent.location})")

    print("\nFind agent by name:")
    found_agent = Agent.get(Agent.name == "agent1")
    print(f"Found: {found_agent.name} in {found_agent.location}")

    print("\nFind agents by location:")
    nyc_agents = Agent.select().where(Agent.location == "NYC")
    for agent in nyc_agents:
        print(f"- {agent.name}")

    # Update
    agent1.location = "SF"
    agent1.save()
    print(f"\nUpdated agent1 location: {Agent.get(Agent.name == 'agent1').location}")

    return agent1  # Return for use in other tests


def test_executor():
    print("\n=== Testing Executor Model ===")

    # Create
    executor1 = Executor.create(name="executor1", description="Test executor 1", state="running")
    executor2 = Executor.create(name="executor2", description="Test executor 2", state="init")

    # Read/Search
    print("All executors:")
    for executor in Executor.select():
        print(f"- {executor.name}: {executor.state}")

    print("\nFind running executors:")
    running = Executor.select().where(Executor.state == "running")
    for executor in running:
        print(f"- {executor.name}")

    # Update
    executor2.state = "running"
    executor2.save()
    print(f"\nUpdated executor2 state: {Executor.get(Executor.name == 'executor2').state}")

    return executor1  # Return for use in other tests


def test_actor(executor):
    print("\n=== Testing Actor Model ===")

    # Create
    actor1 = Actor.create(name="actor1", executor=executor, description="Test actor 1")
    actor2 = Actor.create(name="actor2", executor=executor, description="Test actor 2")

    # Read/Search
    print("All actors:")
    for actor in Actor.select():
        print(f"- {actor.name}: {actor.description} (Executor: {actor.executor.name})")

    print("\nFind actors by executor:")
    executor_actors = Actor.select().join(Executor).where(Executor.name == executor.name)
    for actor in executor_actors:
        print(f"- {actor.name}")

    return actor1  # Return for use in other tests


def test_action(actor):
    print("\n=== Testing Action Model ===")

    # Create
    action1 = Action.create(name="action1", actor=actor, description="Test action 1", code="print('Hello World')")
    action2 = Action.create(name="action2", actor=actor, description="Test action 2", code="print('Goodbye World')")

    # Read/Search
    print("All actions:")
    for action in Action.select():
        print(f"- {action.name}: {action.description} (Actor: {action.actor.name})")

    # Update statistics
    action1.nrok = 5
    action1.nrfailed = 1
    action1.save()
    print(f"\nAction1 stats - Success: {action1.nrok}, Failed: {action1.nrfailed}")

    return action1


def test_job(agent):
    print("\n=== Testing Job Model ===")

    # Create
    job1 = Job.create(
        actor="actor1", action="action1", params='{"param1": "value1"}', job_type="test", executor="executor1", state="running", agent=agent
    )
    job2 = Job.create(
        actor="actor2", action="action2", params='{"param2": "value2"}', job_type="test", executor="executor1", state="init", agent=agent
    )

    # Read/Search
    print("All jobs:")
    for job in Job.select():
        print(f"- Actor: {job.actor}, Action: {job.action}, State: {job.state}")

    print("\nFind running jobs:")
    running_jobs = Job.select().where(Job.state == "running")
    for job in running_jobs:
        print(f"- {job.actor}: {job.action}")

    # Update
    job2.state = "completed"
    job2.completed = True
    job2.finish_date = int(datetime.datetime.now().timestamp())
    job2.save()
    print(f"\nUpdated job2 state: {Job.get(Job.id == job2.id).state}")

    return job1


def test_signature_request(job):
    print("\n=== Testing SignatureRequest Model ===")

    # Create
    sig1 = SignatureRequest.create(job=job, pubkey="ssh-rsa AAAA...", signature="signed-data-1", verified=True)
    sig2 = SignatureRequest.create(job=job, pubkey="ssh-rsa BBBB...", signature="signed-data-2", verified=False)

    # Read/Search
    print("All signature requests:")
    for sig in SignatureRequest.select():
        print(f"- Job: {sig.job.id}, Verified: {sig.verified}")

    print("\nFind verified signatures:")
    verified = SignatureRequest.select().where(SignatureRequest.verified == True)
    for sig in verified:
        print(f"- {sig.pubkey}")


def test_job_log(job):
    print("\n=== Testing JobLog Model ===")

    # Create
    log1 = JobLog.create(job=job, log_sequence=1, message="Started job", category="info")
    log2 = JobLog.create(job=job, log_sequence=2, message="Processing...", category="debug")
    log3 = JobLog.create(job=job, log_sequence=3, message="Completed successfully", category="info")

    # Read/Search
    print("All logs for job:")
    logs = JobLog.select().where(JobLog.job == job).order_by(JobLog.log_sequence)
    for log in logs:
        print(f"- [{log.category}] {log.message}")

    print("\nFind info logs:")
    info_logs = JobLog.select().where((JobLog.job == job) & (JobLog.category == "info"))
    for log in info_logs:
        print(f"- {log.message}")


def main():
    setup_database()

    # Run tests in order due to foreign key relationships
    agent = test_agent()
    executor = test_executor()
    actor = test_actor(executor)
    action = test_action(actor)
    job = test_job(agent)
    test_signature_request(job)
    test_job_log(job)

    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    main()

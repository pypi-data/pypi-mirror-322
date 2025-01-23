import os
import yaml
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from server import *

@dataclass
class EnvVariable:
    key: str
    value: str

@dataclass
class HandlerCommand:
    command: str

@dataclass
class Handlers:
    success: Optional[HandlerCommand] = None
    failure: Optional[HandlerCommand] = None
    cancel: Optional[HandlerCommand] = None
    exit: Optional[HandlerCommand] = None

@dataclass
class RepeatPolicy:
    repeat: bool
    intervalSec: int

@dataclass
class Precondition:
    condition: str
    expected: str

@dataclass
class Step:
    name: str
    command: str
    script: Optional[str] = None
    depends: List[str] = field(default_factory=list)
    description: Optional[str] = None
    repeatPolicy: Optional[RepeatPolicy] = None

@dataclass
class DAG:
    name: str
    description: Optional[str] = None
    schedule: Optional[str] = None
    group: Optional[str] = None
    tags: Optional[str] = None  # This should be a single string
    env: Dict[str, str] = field(default_factory=dict)
    logDir: Optional[str] = None
    restartWaitSec: Optional[int] = None
    histRetentionDays: Optional[int] = None
    delaySec: Optional[int] = None
    maxActiveRuns: Optional[int] = None
    params: Optional[List[str]] = field(default_factory=list)
    preconditions: List[Precondition] = field(default_factory=list)
    mailOn: Dict[str, bool] = field(default_factory=dict)
    handlerOn: Handlers = field(default_factory=Handlers)
    MaxCleanUpTimeSec: Optional[int] = None
    steps: List[Step] = field(default_factory=list)

    def add_step(self, step: Step):
        """Add a step to the DAG."""
        self.steps.append(step)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            **({"description": self.description} if self.description else {}),
            **({"schedule": self.schedule} if self.schedule else {}),
            **({"group": self.group} if self.group else {}),
            **({"tags": self.tags} if self.tags else {}),
            **({"env": [{"key": k, "value": v} for k, v in self.env.items()]} if self.env else {}),
            **({"logDir": self.logDir} if self.logDir else {}),
            **({"restartWaitSec": self.restartWaitSec} if self.restartWaitSec else {}),
            **({"histRetentionDays": self.histRetentionDays} if self.histRetentionDays else {}),
            **({"delaySec": self.delaySec} if self.delaySec else {}),
            **({"maxActiveRuns": self.maxActiveRuns} if self.maxActiveRuns else {}),
            **({"params": " ".join(self.params)} if self.params else {}),
            **({"preconditions": [{"condition": pc.condition, "expected": pc.expected} for pc in self.preconditions]} if self.preconditions else {}),
            **({"mailOn": self.mailOn} if self.mailOn else {}),
            **({"MaxCleanUpTimeSec": self.MaxCleanUpTimeSec} if self.MaxCleanUpTimeSec else {}),
            **({"handlerOn": {
                "success": {"command": self.handlerOn.success.command} if self.handlerOn.success else None,
                "failure": {"command": self.handlerOn.failure.command} if self.handlerOn.failure else None,
                "cancel": {"command": self.handlerOn.cancel.command} if self.handlerOn.cancel else None,
                "exit": {"command": self.handlerOn.exit.command} if self.handlerOn.exit else None,
            }} if any(vars(self.handlerOn).values()) else {}),
            "steps": [
                {
                    "name": step.name,
                    "command": step.command,
                    **({"script": step.script} if step.script else {}),
                    **({"depends": step.depends} if step.depends else {}),  # Change this back to depends_on if needed
                    **({"description": step.description} if step.description else {}),
                    **({"repeatPolicy": {
                        "repeat": step.repeatPolicy.repeat,
                        "intervalSec": step.repeatPolicy.intervalSec
                    }} if step.repeatPolicy else {}),
                } for step in self.steps
            ],
        }

    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict(), sort_keys=False)

def new(**kwargs) -> DAG:
    return DAG(**kwargs)

# Example usage to create a new DAG
if __name__ == "__main__":
    # Initialize the server with the default DAG directory
    server = Server()

    # List existing DAGs
    print("Listing existing DAGs:")
    dags = server.list_dags()
    for dag_name in dags:
        print(f" - {dag_name}")

    # Create a new DAG
    dag = new(
        name="example_dag",
        description="Example DAG to demonstrate functionality",
        schedule="0 * * * *",
        group="ExampleGroup",
        tags="example",  # Convert tags to a comma-separated string
        env={
            "LOG_DIR": "${HOME}/logs",
            "PATH": "/usr/local/bin:${PATH}"
        },
        logDir="${LOG_DIR}",
        restartWaitSec=60,
        histRetentionDays=3,
        delaySec=1,
        maxActiveRuns=1,
        params=["param1", "param2"],
        preconditions=[
            Precondition(condition="`echo $2`", expected="param2")
        ],
        mailOn={"failure": True, "success": True},
        MaxCleanUpTimeSec=300,
        handlerOn=Handlers(
            success=HandlerCommand(command="echo succeed"),  # Convert to map structure
            failure=HandlerCommand(command="echo failed"),  # Convert to map structure
            cancel=HandlerCommand(command="echo canceled"),  # Convert to map structure
            exit=HandlerCommand(command="echo finished")  # Convert to map structure
        )
    )

    # Add steps to the DAG
    dag.add_step(Step(
        name="pull_data",
        command="sh",
        script="echo `date '+%Y-%m-%d'`",
    ))

    dag.add_step(Step(
        name="cleanse_data",
        command="echo cleansing ${DATA_DIR}/${DATE}.csv",
        depends=["pull_data"]  # Ensure this is the correct key
    ))

    dag.add_step(Step(
        name="transform_data",
        command="echo transforming ${DATA_DIR}/${DATE}_clean.csv",
        depends=["cleanse_data"]  # Ensure this is the correct key
    ))

    dag.add_step(Step(
        name="A task",
        command="main.sh",
        repeatPolicy=RepeatPolicy(repeat=True, intervalSec=60)
    ))

    # Save the new DAG as a YAML file
    server.create_dag(dag)
    print(f"DAG '{dag.name}' created and saved and started.")

    # List DAGs again to see the newly created one
    print("\nListing updated DAGs:")
    dags = server.list_dags()
    for dag_name in dags:
        print(f" - {dag_name}")

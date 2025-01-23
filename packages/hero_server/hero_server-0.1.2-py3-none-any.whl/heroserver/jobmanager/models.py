import datetime

from peewee import (
    SQL,
    BigIntegerField,
    BooleanField,
    CharField,
    Check,
    DatabaseProxy,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

database = DatabaseProxy()  # Will be initialized in db.py


class BaseModel(Model):
    class Meta:
        database = database


class Agent(BaseModel):
    name = CharField(unique=True)
    description = TextField(null=True)
    ipaddr = CharField(null=True)
    pubkey = TextField(null=True)
    location = CharField(null=True)
    create_date = BigIntegerField(default=lambda: int(datetime.datetime.now().timestamp()))

    class Meta:
        indexes = (
            (("name",), True),  # unique index
            (("pubkey",), False),  # non-unique index
        )


class Executor(BaseModel):
    name = CharField(unique=True)
    description = TextField(null=True)
    state = CharField(default="init", constraints=[Check("state in ('init', 'running', 'error', 'halted')")])

    class Meta:
        indexes = (
            (("name",), True),
            (("state",), False),
        )


class Actor(BaseModel):
    name = CharField(unique=True)
    executor = ForeignKeyField(Executor, backref="actors", on_delete="CASCADE")
    description = TextField(null=True)

    class Meta:
        indexes = ((("name",), True),)


class Action(BaseModel):
    name = CharField()
    actor = ForeignKeyField(Actor, backref="actions", on_delete="CASCADE")
    description = TextField(null=True)
    nrok = IntegerField(default=0)
    nrfailed = IntegerField(default=0)
    code = TextField(null=True)

    class Meta:
        indexes = ((("name",), False),)


class Job(BaseModel):
    actor = CharField()
    action = CharField()
    params = TextField(null=True)  # JSON string
    job_type = CharField()
    executor = CharField(null=True)
    create_date = BigIntegerField(default=lambda: int(datetime.datetime.now().timestamp()))
    schedule_date = BigIntegerField(default=lambda: int(datetime.datetime.now().timestamp()))
    finish_date = BigIntegerField(null=True)
    locked_until = BigIntegerField(null=True)
    completed = BooleanField(default=False)
    state = CharField(default="init")
    error = TextField(null=True)
    recurring = CharField(default="")
    deadline = BigIntegerField(null=True)
    signature = TextField(null=True)
    agent = ForeignKeyField(Agent, backref="jobs", null=True, on_delete="SET NULL")

    class Meta:
        indexes = (
            (("actor",), False),
            (("action",), False),
            (("job_type",), False),
            (("state",), False),
            (("schedule_date",), False),
            (("finish_date",), False),
            (("executor",), False),
        )


class SignatureRequest(BaseModel):
    job = ForeignKeyField(Job, backref="signature_requests", on_delete="CASCADE")
    pubkey = TextField()
    signature = TextField()
    date = BigIntegerField(default=lambda: int(datetime.datetime.now().timestamp()))
    verified = BooleanField(default=False)

    class Meta:
        indexes = (
            (("job",), False),
            (("pubkey",), False),
        )


class JobLog(BaseModel):
    job = ForeignKeyField(Job, backref="logs", on_delete="CASCADE")
    log_sequence = IntegerField()
    message = TextField()
    category = CharField()
    log_time = BigIntegerField(default=lambda: int(datetime.datetime.now().timestamp()))

    class Meta:
        indexes = (
            (("job",), False),
            (("category",), False),
            (("message",), False),
        )
        constraints = [SQL("UNIQUE (job_id, log_sequence)")]


MODELS = [Agent, Executor, Actor, Action, Job, SignatureRequest, JobLog]

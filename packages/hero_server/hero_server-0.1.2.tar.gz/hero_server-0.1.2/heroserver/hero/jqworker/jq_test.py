from rq import Queue
from redis import Redis
from rq.job import Job
from jqworker.count import *
from rq.serializers import JSONSerializer
import time

# Tell RQ what Redis connection to use
connection = Redis()

q = Queue(connection=connection)

job = q.enqueue(count_words_at_url, 'http://nvie.com')



s=EmailConfig(name="myname")
print(s)

job2 = q.enqueue(struct_echo, s)

time.sleep(3)

print(job.result)   # => None  # Changed to job.return_value() in RQ >= 1.12.0
print(job2.result)   # => None  # Changed to job.return_value() in RQ >= 1.12.0


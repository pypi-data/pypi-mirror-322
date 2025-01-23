import os
import tempfile
import unittest
from datetime import datetime

from heroserver.jobmanager.ManagerJobs import ManagerJobs
from heroserver.jobmanager.models import Job, JobState, JobType


class TestJobQueue(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.jq = ManagerJobs(self.db_path)

    def tearDown(self):
        # Close the database connection and remove the temporary file
        self.jq.__del__()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_create_and_get_job(self):
        # Create a test job
        job_params = '{"test_param": "test_value"}'
        new_job = Job(
            actor="TestActor",
            action="test_action",
            params=job_params,
            job_type=JobType.HEROSCRIPT,
        )

        # Add job to queue
        job_id = self.jq.set_job(new_job)
        self.assertIsNotNone(job_id)

        # Retrieve the job
        retrieved_job = self.jq.get_job_queued()
        self.assertIsNotNone(retrieved_job)
        self.assertEqual(retrieved_job.actor, "TestActor")
        self.assertEqual(retrieved_job.action, "test_action")
        self.assertEqual(retrieved_job.params, '{"test_param": "test_value"}')
        self.assertEqual(retrieved_job.job_type.value, JobType.HEROSCRIPT.value)
        self.assertFalse(retrieved_job.completed)

    def test_complete_job(self):
        # Create and get a job
        job = Job(actor="TestActor", action="test_action", params="{}")
        job_id = self.jq.set_job(job)
        retrieved_job = self.jq.get_job_queued()

        # Complete the job
        self.jq.complete_job(str(job_id), success=True)

        # Try to get the job again - should return None as it's completed
        next_job = self.jq.get_job_queued()
        self.assertIsNone(next_job)

    def test_recurring_job(self):
        # Create a recurring job scheduled for now
        now = datetime.now()
        job = Job(
            actor="TestActor",
            action="test_action",
            params="{}",
            recurring="0 5 * * *",  # Every day at 5 AM
            schedule_date=int(now.timestamp()),
        )
        job_id = self.jq.set_job(job)

        # Get and complete the job
        retrieved_job = self.jq.get_job_queued()
        self.assertIsNotNone(retrieved_job)
        self.jq.complete_job(str(job_id), success=True)

        # Verify the next job was created but is scheduled for the future
        cursor = self.jq.conn.execute("SELECT * FROM job_queue WHERE completed = 0")
        next_job_row = cursor.fetchone()
        self.assertIsNotNone(next_job_row)
        self.assertEqual(next_job_row["actor"], "TestActor")
        self.assertEqual(next_job_row["action"], "test_action")
        self.assertEqual(next_job_row["state"], JobState.INIT.value)

        # Verify it's scheduled for the future
        schedule_date = datetime.fromtimestamp(next_job_row["schedule_date"])
        self.assertGreater(schedule_date, datetime.now())

    def test_job_locking(self):
        # Create a job queue in a new connection
        jq1 = ManagerJobs(self.db_path)

        # Create a job
        job = Job(actor="TestActor", action="test_action", params="{}")
        job_id = jq1.set_job(job)

        # Get the job with a lock in the first connection
        first_job = jq1.get_job_queued(execution_time=2)
        self.assertIsNotNone(first_job)
        self.assertEqual(first_job.actor, "TestActor")

        # Try to get the same job in a second connection
        jq2 = ManagerJobs(self.db_path)
        second_job = jq2.get_job_queued()
        self.assertIsNone(second_job, "Job should be locked and not available")

        # Clean up
        jq1.__del__()
        jq2.__del__()

    def test_logging(self):
        # Create a job
        job = Job(actor="TestActor", action="test_action", params="{}")
        job_id = self.jq.set_job(job)

        # Add some logs
        log1_id = self.jq.add_log(str(job_id), "Starting job", "info")
        log2_id = self.jq.add_log(str(job_id), "Processing data", "debug")
        log3_id = self.jq.add_log(str(job_id), "Error occurred", "error")

        # Test getting logs for job
        logs = self.jq.get_logs(str(job_id))
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[0]["message"], "Starting job")
        self.assertEqual(logs[0]["category"], "info")
        self.assertEqual(logs[0]["log_sequence"], 1)

        # Test getting logs by category
        error_logs = self.jq.get_logs(str(job_id), "error")
        self.assertEqual(len(error_logs), 1)
        self.assertEqual(error_logs[0]["message"], "Error occurred")

        # Test searching logs
        search_results = self.jq.search_logs("Processing")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]["message"], "Processing data")

        # Test deleting logs
        deleted = self.jq.delete_logs(str(job_id))
        self.assertEqual(deleted, 3)

        # Verify logs were deleted
        remaining_logs = self.jq.get_logs(str(job_id))
        self.assertEqual(len(remaining_logs), 0)

    def test_error_handling(self):
        # Create a job
        job = Job(actor="TestActor", action="test_action", params="{}")
        job_id = self.jq.set_job(job)

        # Complete job with error
        error_msg = "Test error message"
        self.jq.complete_job(str(job_id), success=False, error=error_msg)

        # Job should be marked as completed with error
        cursor = self.jq.conn.execute("SELECT * FROM job_queue WHERE id = ?", (job_id,))
        job_row = cursor.fetchone()
        self.assertEqual(job_row["state"], JobState.ERROR.value)
        self.assertEqual(job_row["error"], error_msg)
        self.assertTrue(job_row["completed"])


if __name__ == "__main__":
    unittest.main()

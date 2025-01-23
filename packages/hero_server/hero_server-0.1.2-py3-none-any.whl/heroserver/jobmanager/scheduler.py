import importlib
import multiprocessing
import sys
import time
from typing import Tuple

from heroserver.jobmanager.ManagerJobs import ManagerJobs
from heroserver.jobmanager.models import Job


class JobScheduler:
    def __init__(self, db_path: str):
        """Initialize the job scheduler.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._should_stop = multiprocessing.Value("b", False)
        self._registered_functions = {}
        self.job_queue = None

    def register_function(self, actor: str, action: str, module_name: str, function_name: str):
        """Register a function for a specific actor and action.

        Args:
            actor: Name of the actor (e.g., "EchoService")
            action: Name of the action (e.g., "echo")
            module_name: Name of module containing the function
            function_name: Name of function to execute
        """
        if actor not in self._registered_functions:
            self._registered_functions[actor] = {}
        self._registered_functions[actor][action] = (module_name, function_name)

    def unregister_function(self, actor: str, action: str):
        """Unregister a function.

        Args:
            actor: Name of the actor
            action: Name of the action
        """
        if actor in self._registered_functions:
            if action in self._registered_functions[actor]:
                del self._registered_functions[actor][action]
            if not self._registered_functions[actor]:
                del self._registered_functions[actor]

    def _execute_job(self, job: Job) -> Tuple[bool, str]:
        """Execute a job in the current process.

        Args:
            job: Job to execute

        Returns:
            Tuple[bool, str]: Success status and error message if any
        """
        print(f"\n{'='*60}")
        print(f"Executing job {job.id}: {job.actor}.{job.action}")
        print(f"Parameters: {job.params}")
        print(f"{'='*60}\n")

        if job.actor not in self._registered_functions:
            error = f"No functions registered for actor: {job.actor}"
            print(f"Error: {error}")
            return False, error

        if job.action not in self._registered_functions[job.actor]:
            error = f"No function registered for action: {job.action} in actor: {job.actor}"
            print(f"Error: {error}")
            return False, error

        module_name, function_name = self._registered_functions[job.actor][job.action]
        print(f"Looking for function {function_name} in module {module_name}")

        try:
            try:
                print(f"Attempting import from examples package: examples.{module_name}")
                module = importlib.import_module(f"examples.{module_name}")
                print(f"Successfully imported examples.{module_name}")
            except ImportError as e:
                print(f"Examples import failed: {e}")
                # Try importing directly
                try:
                    print(f"Attempting direct import of {module_name}")
                    module = importlib.import_module(module_name)
                    print(f"Successfully imported {module_name}")
                except ImportError as e:
                    error = f"Failed to import module {module_name}: {e}"
                    print(f"Error: {error}")
                    return False, error

            print(f"Getting function {function_name} from module {module.__name__}")
            func = getattr(module, function_name)
            print(f"Found function {function_name}")
            print(f"Function parameters: {job.params}")

            try:
                print(f"Executing {function_name}...")
                func(**job.params)
                print(f"Job {job.id} executed successfully")
                return True, ""
            except Exception as e:
                error = f"Function execution failed: {str(e)}"
                print(f"Error: {error}")
                return False, error
        except Exception as e:
            error = f"Job execution error: {str(e)}"
            print(f"Error: {error}")
            return False, error

    def _process_job(self, job: Job, queue: ManagerJobs):
        """Process a job.

        Args:
            job: Job to process
            queue: ManagerJobs instance to use
        """
        try:
            print(f"\nProcessing job {job.id}")
            success, error = self._execute_job(job)

            # Complete the job
            queue.complete_job(job.id, success=success, error=error)
            print(f"Job {job.id} marked as {'succeeded' if success else 'failed'}")

            # Show job status
            if success:
                print(f"Job {job.id} completed successfully")
            else:
                print(f"Job {job.id} failed: {error}")

            # Get updated counts
            failed = queue.get_failed_jobs()
            succeeded = queue.get_succeeded_jobs()
            print(f"Current status: {len(succeeded)} succeeded, {len(failed)} failed")
        except Exception as e:
            error_msg = f"Error processing job {job.id}: {str(e)}"
            print(error_msg)
            queue.complete_job(job.id, success=False, error=error_msg)

    def _scheduler_process(self, registered_functions, python_path, run_duration: float, poll_interval: float = 1.0):
        """Main scheduler process function.

        Args:
            registered_functions: Copy of registered functions
            python_path: List of paths to add to sys.path
            run_duration: Maximum time to run in seconds (0 for unlimited)
            poll_interval: Time in seconds to wait between polling for new jobs
        """
        try:
            # Update Python path in worker process
            for path in python_path:
                if path not in sys.path:
                    sys.path.insert(0, path)
                    print(f"Added to Python path: {path}")

            # Create ManagerJobs instance in the scheduler process
            queue = ManagerJobs(self.db_path)
            self._registered_functions = registered_functions

            print(f"Worker process Python path: {sys.path}")
            print(f"Registered functions: {self._registered_functions}")
            print(f"Run duration: {run_duration if run_duration > 0 else 'unlimited'} seconds")

            start_time = time.time()
            last_job_time = start_time

            while not self._should_stop.value:
                try:
                    # Check if we should stop based on duration
                    if run_duration > 0 and (time.time() - start_time) >= run_duration:
                        print(f"\nRun duration of {run_duration} seconds exceeded")
                        break

                    # Get a job with a short lock time
                    job = queue.get_job(execution_time=10)
                    if job:
                        print(f"\nProcessing job {job.id}: {job.actor}.{job.action}")
                        self._process_job(job, queue)
                        print(f"Finished processing job {job.id}")
                        last_job_time = time.time()

                        # Show current job status
                        waiting = queue.get_waiting_jobs()
                        failed = queue.get_failed_jobs()
                        succeeded = queue.get_succeeded_jobs()
                        print(f"Current status: {len(waiting)} waiting, {len(failed)} failed, {len(succeeded)} succeeded")
                    else:
                        # If no jobs and we've waited more than 5 seconds since last job
                        if time.time() - last_job_time > 5:
                            waiting = queue.get_waiting_jobs()
                            if not waiting:
                                print("\nNo jobs waiting and no activity for 5 seconds")
                                break
                except Exception as e:
                    print(f"Error in scheduler loop: {e}")
                time.sleep(poll_interval)
        except Exception as e:
            print(f"Fatal error in scheduler process: {e}")
        finally:
            queue.conn.close()

    def start(self, run_duration: float = 60.0, poll_interval: float = 1.0):
        """Start the job scheduler.

        Args:
            run_duration: Maximum time to run in seconds (0 for unlimited). Defaults to 60 seconds.
            poll_interval: Time in seconds to wait between polling for new jobs
        """
        with self._should_stop.get_lock():
            self._should_stop.value = False

        # Get current Python path
        python_path = sys.path.copy()

        # Start scheduler in a new process
        scheduler_process = multiprocessing.Process(
            target=self._scheduler_process, args=(self._registered_functions.copy(), python_path, run_duration, poll_interval)
        )
        scheduler_process.start()
        return scheduler_process

    def stop(self):
        """Stop the job scheduler."""
        with self._should_stop.get_lock():
            self._should_stop.value = True

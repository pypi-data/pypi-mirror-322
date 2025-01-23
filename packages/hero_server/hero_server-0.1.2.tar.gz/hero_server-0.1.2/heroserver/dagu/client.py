import os
import requests
from requests.auth import HTTPBasicAuth
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import time

@dataclass
class DAGStatus:
    name: str
    status: str
    group: Optional[str] = None
    schedule: Optional[str] = None
    lastRun: Optional[str] = None
    nextRun: Optional[str] = None
    pid: Optional[int] = None
    log: Optional[str] = None
    requestId: Optional[str] = None
    params: Optional[str] = None
    startedAt: Optional[str] = None
    finishedAt: Optional[str] = None
    suspended: Optional[bool] = None

    def get_last_run_epoch(self) -> Optional[int]:
        """Convert lastRun to epoch time."""
        return self._convert_to_epoch(self.lastRun)

    def get_next_run_epoch(self) -> Optional[int]:
        """Convert nextRun to epoch time."""
        return self._convert_to_epoch(self.nextRun)

    @staticmethod
    def _convert_to_epoch(timestamp: Optional[str]) -> Optional[int]:
        """Helper method to convert an ISO 8601 timestamp to epoch time."""
        if timestamp:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return int(time.mktime(dt.timetuple()))
        return None

class DAGuClient:
    def __init__(self, base_url: str = "http://localhost:8888"):
        self.base_url = base_url
        self.auth = self._get_basic_auth()

    def _get_basic_auth(self) -> HTTPBasicAuth:
        """Retrieve the Basic Auth credentials from environment variables."""
        username = os.getenv('DAGU_BASICAUTH_USERNAME')
        password = os.getenv('DAGU_BASICAUTH_PASSWORD')

        if not username or not password:
            raise EnvironmentError("Please set the DAGU_BASICAUTH_USERNAME and DAGU_BASICAUTH_PASSWORD environment variables.")

        return HTTPBasicAuth(username, password)

    def list_dags(self) -> List[DAGStatus]:
        """Fetches the list of DAGs with their statuses from the DAGu REST API."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/dags", auth=self.auth)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            dags_data = response.json().get('DAGs', [])

            if isinstance(dags_data, list):
                return [self._parse_dag(dag) for dag in dags_data]
            else:
                print(f"Unexpected response format: {dags_data}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return []

    def _parse_dag(self, dag_entry: dict) -> DAGStatus:
        """Helper function to parse a DAG's JSON data into a DAGStatus object."""
        try:
            dag_data = dag_entry.get("DAG", {})
            status_data = dag_entry.get("Status", {})

            return DAGStatus(
                name=dag_data.get("Name"),
                status=status_data.get("StatusText"),
                group=dag_data.get("Group"),
                schedule=(dag_data.get("Schedule", [{}])[0].get("Expression") 
                          if dag_data.get("Schedule") else None),
                lastRun=status_data.get("FinishedAt"),
                nextRun=None,  # Adjust as needed based on your API's response format
                pid=status_data.get("Pid"),
                log=status_data.get("Log"),
                requestId=status_data.get("RequestId"),
                params=status_data.get("Params"),
                startedAt=status_data.get("StartedAt"),
                finishedAt=status_data.get("FinishedAt"),
                suspended=dag_entry.get("Suspended")
            )
        except AttributeError as e:
            print(f"Error parsing DAG data: {dag_entry}, Error: {e}")
            return None

    def submit_dag_action(self, name: str, action: str, request_id: Optional[str] = None, params: Optional[str] = None) -> dict:
        """Submit an action to a specified DAG.
        
        Args:
            name (str): Name of the DAG.
            action (str): Action to be performed ('start', 'stop', or 'retry').
            request_id (Optional[str]): Required if action is 'retry'.
            params (Optional[str]): Parameters for the DAG execution.

        Returns:
            dict: Response from the API.
        """
        url = f"{self.base_url}/api/v1/dags/{name}"
        payload = {
            "action": action,
            **({"request-id": request_id} if request_id else {}),
            **({"params": params} if params else {}),
        }

        try:
            response = requests.post(url, json=payload, auth=self.auth)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            print(f"Response content: {response.content}")
            return {}

# Example usage
if __name__ == "__main__":
    client = DAGuClient()
    
    # List DAGs
    try:
        dags = client.list_dags()
        for dag in dags:
            if dag:
                print(f"DAG Name: {dag.name}, Status: {dag.status}, Group: {dag.group}, "
                      f"Schedule: {dag.schedule}, Last Run: {dag.lastRun}, "
                      f"Next Run: {dag.nextRun}, PID: {dag.pid}, Log: {dag.log}, "
                      f"Request ID: {dag.requestId}, Params: {dag.params}, "
                      f"Started At: {dag.startedAt}, Finished At: {dag.finishedAt}, "
                      f"Suspended: {dag.suspended}")
                # Example of using helper methods to get epoch times
                if dag.get_last_run_epoch():
                    print(f"Last Run Epoch: {dag.get_last_run_epoch()}")
                if dag.get_next_run_epoch():
                    print(f"Next Run Epoch: {dag.get_next_run_epoch()}")
    except Exception as e:
        print(f"Error: {e}")

    # Submit an action to a DAG (example: start a DAG)
    try:
        dag_name = "test11"  # Replace with your actual DAG name
        action_response = client.submit_dag_action(name=dag_name, action="start")
        print(f"Action Response: {action_response}")
    except Exception as e:
        print(f"Error: {e}")

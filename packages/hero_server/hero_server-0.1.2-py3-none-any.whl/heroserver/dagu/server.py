import os
import yaml
import glob
from typing import List
from dag import DAG
from client import *

# Assuming the following classes have already been defined:
# - DAG (for creating and managing DAG structures)
# - Step
# - Handlers
# - RepeatPolicy
# - Precondition

class Server:
    def __init__(self, dag_dir: str = "~/hero/var/dagu/dags/"):
        self.dag_dir = os.path.expanduser(dag_dir)
        os.makedirs(self.dag_dir, exist_ok=True)  # Ensure the directory exists

    def list_dags(self) -> List[str]:
        """Lists the DAGs in the directory."""
        dag_files = glob.glob(os.path.join(self.dag_dir, "*.yaml"))
        return [os.path.splitext(os.path.basename(dag_file))[0] for dag_file in dag_files]

    def delete_dag(self, name: str) -> bool:
        """Deletes a DAG file based on its name."""
        dag_file = os.path.join(self.dag_dir, f"{name}.yaml")
        if os.path.exists(dag_file):
            os.remove(dag_file)
            return True
        else:
            print(f"DAG '{name}' does not exist.")
            return False

    def create_dag(self, dag:DAG, start:bool = True) -> bool:
        """Creates a new DAG and saves it as a YAML file."""
        dag_file = os.path.join(self.dag_dir, f"{dag.name}.yaml")
        with open(dag_file, 'w') as file:
            yaml.dump(dag.to_dict(), file, sort_keys=False)
        if start:
            self.start_dag(dag.name)
        return True
    
    def start_dag(self,dag_name:str) -> bool:
        client = DAGuClient()
        action_response = client.submit_dag_action(name=dag_name, action="start")
        
    def stop_dag(self,dag_name:str) -> bool:
        client = DAGuClient()
        action_response = client.submit_dag_action(name=dag_name, action="stop")        
        

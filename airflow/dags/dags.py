import os
import airflow
from gusty import GustyDAG

#####################
## DAG Directories ##
#####################

# point to your dags directory
dag_parent_dir = os.path.join(os.environ['AIRFLOW_HOME'], "dags")

# assumes any subdirectories in the dags directory are Gusty DAGs (with METADATA.yml) (excludes subdirectories like __pycache__)
dag_directories = [os.path.join(dag_parent_dir, name) for name in os.listdir(dag_parent_dir) if os.path.isdir(os.path.join(dag_parent_dir, name)) and not name.endswith('__')]

####################
## DAG Generation ##
####################

for dag_directory in dag_directories:
    dag_id = os.path.basename(dag_directory)
    globals()[dag_id] = GustyDAG(dag_directory)

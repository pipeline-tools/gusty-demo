# This DAG lines up one-to-one with the Airflow tutorial:
# https://airflow.apache.org/docs/stable/tutorial.html

import os
from gusty import GustyDAG

dag_directory = os.path.splitext(os.path.abspath(__file__))[0]
dag = GustyDAG(dag_directory)

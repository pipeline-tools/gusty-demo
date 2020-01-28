import os
import re
import pandas as pd

from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.utils.decorators import apply_defaults

from .operator_utils.job_colors import job_colors

from . import register_build

#############
## Globals ##
#############

dags_dir = os.path.join(os.getenv('AIRFLOW_HOME'), "dags")

###############
## Functions ##
###############

###############
## Operators ##
###############

class JupyterOperator(SSHOperator):
    """
    The JupyterOperator executes a Jupyter notebook file. Note that it is up to
    the ipynb itself to handle connecting to the database.
    """
    @apply_defaults
    def __init__(self, file_path, **kwargs):
        self.ipynb_file = file_path
        self.ui_color = job_colors["ipynb"]

        # The volume is shared at the same location with the pythonserver container
        self.command = '(jupyter nbconvert --to script --execute --stdout %s | python)' % (self.ipynb_file, )

        super(JupyterOperator, self).__init__(
            command = self.command,
            ssh_conn_id = "ssh_pythonserver",
            **kwargs)

###################
## Task Builders ##
###################

def build_ipynb_task(**kwargs):
    task = JupyterOperator(
        task_id=kwargs["spec"]["task_id"],
        dag=kwargs["dag"],
        file_path=kwargs["spec"]["file_path"]
        )
    return task

####################
## Register Build ##
####################

register_build(build_ipynb_task)

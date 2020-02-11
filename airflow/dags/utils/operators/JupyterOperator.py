import os
import re
import pandas as pd

from airflow.operators.bash_operator import BashOperator
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

class JupyterOperator(BashOperator):
    """
    The JupyterOperator executes a Jupyter notebook file. Note that it is up to
    the ipynb itself to handle connecting to the database.
    """
    @apply_defaults
    def __init__(self, file_path, **kwargs):
        self.ipynb_file = file_path
        self.html_output = file_path.replace('.ipynb', '.html')
        self.user = os.environ['EZ_AF_USER']
        self.pythonserver = os.environ['EZ_AF_PYTHON_SERVER']
        self.ui_color = job_colors["ipynb"]

        self.command = """(scp -o StrictHostKeyChecking=no {local_filepath} {user}@{pythonserver}:~/
                           ssh -o StrictHostKeyChecking=no {user}@{pythonserver} 'jupytext --execute ~/{filepath_basename}' || exit 1;
                           ssh -o StrictHostKeyChecking=no {user}@{pythonserver} 'rm ~/{filepath_basename} && rm -f ~/{html_output_basename}';
                           )""".format(
                           user = self.user,
                           pythonserver = self.pythonserver,
                           local_filepath = self.ipynb_file,
                           filepath_basename = os.path.basename(self.ipynb_file),
                           html_output_basename = os.path.basename(self.html_output))

        super(JupyterOperator, self).__init__(
            bash_command = self.command,
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

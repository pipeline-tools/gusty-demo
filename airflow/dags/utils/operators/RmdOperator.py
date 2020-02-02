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

class RmdOperator(BashOperator):
    """
    The RmdOperator executes the R Markdown file. Note that it is up to the Rmd itself
    to handle connecting to the database.
    """
    @apply_defaults
    def __init__(self, file_path, **kwargs):
        self.rmd_file = file_path
        self.html_output = file_path.replace('.Rmd', '.html')
        self.user = os.environ['EZ_AF_USER']
        self.rserver = os.environ['EZ_AF_R_SERVER']
        self.ui_color = job_colors["rmd"]

        self.command = """(scp -o StrictHostKeyChecking=no {local_filepath} {user}@{rserver}:~/
                           ssh -o StrictHostKeyChecking=no {user}@{rserver} 'Rscript /usr/render_rmd.R ~/{filepath_basename}';
                           ssh -o StrictHostKeyChecking=no {user}@{rserver} 'rm ~/{filepath_basename} && rm ~/{html_output_basename}';
                           )""".format(
                           user = self.user,
                           rserver = self.rserver,
                           local_filepath = self.rmd_file,
                           filepath_basename = os.path.basename(self.rmd_file),
                           html_output_basename = os.path.basename(self.html_output))

        super(RmdOperator, self).__init__(
            bash_command = self.command,
            **kwargs)

###################
## Task Builders ##
###################

def build_rmd_task(**kwargs):
    task = RmdOperator(
        task_id=kwargs["spec"]["task_id"],
        dag=kwargs["dag"],
        file_path=kwargs["spec"]["file_path"]
        )
    return task

####################
## Register Build ##
####################

register_build(build_rmd_task)

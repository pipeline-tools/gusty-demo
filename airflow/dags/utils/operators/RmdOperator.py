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

class RmdOperator(SSHOperator):
    """
    The RmdOperator executes the R Markdown file. Note that it is up to the Rmd itself
    to handle connecting to the database.
    """
    @apply_defaults
    def __init__(self, file_path, **kwargs):
        self.rmd_file = file_path
        self.ui_color = job_colors["rmd"]
        
        # The volume is shared at the same location with the rserver container 
        self.command = ("Rscript -e 'library(methods); rmarkdown::render(\"%s\")'" %
          (self.rmd_file, ))
        
        super(RmdOperator, self).__init__(
            command = self.command,
            ssh_conn_id = "ssh_rserver",
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

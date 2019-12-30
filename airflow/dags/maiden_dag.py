import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago

from utils.taskmaker import *

##############
## DAG Name ##
##############

dag_name = os.path.splitext(os.path.basename(__file__))[0]

##################
## Default Args ##
##################

default_args = {
    'owner': 'Chris',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['hipsterlogic23@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

#########
## DAG ##
#########

dag = DAG(
    dag_name,
    default_args = default_args,
    schedule_interval= "1 0 * * *"
)

###########
## Tasks ##
###########

yaml_specs = get_yaml_specs(dag_name=dag_name)
tasks = build_tasks(yaml_specs, dag=dag)
set_dependencies(yaml_specs, tasks, dag=dag)

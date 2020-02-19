import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago

from gusty import *

##############
## DAG Info ##
##############

dag_directory = os.path.splitext(os.path.abspath(__file__))[0]
dag_name = os.path.basename(dag_directory)

##################
## Default Args ##
##################

default_args = {
    'owner': 'You',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['your_email@gmail.com'],
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

build_dag(dag_directory, dag)

import os
import re
import pandas as pd

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from .operator_utils.db_connections import get_datalake_engine
from .operator_utils.job_colors import job_colors

from . import register_build

#############
## Globals ##
#############

dags_dir = os.path.join(os.getenv('AIRFLOW_HOME'), "dags")
csv_dir = os.path.join(dags_dir, "csv")
csv_files = [os.path.join(csv_dir, file) for file in os.listdir(csv_dir) if file.endswith("csv")]

###############
## Functions ##
###############

def clean_columns(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.map(lambda x: re.sub('[^0-9a-zA-Z_]+', '', x))
    df.columns = df.columns.map(lambda x: re.sub('_+', '_', x))
    return df

def import_csv(csv_file, table_name):
    csv_path = os.path.join(csv_dir, csv_file)
    assert csv_path in csv_files, "CSV file " + csv_file + " does not exist in " + csv_dir
    csv_file = pd.read_csv(csv_path)
    csv_file = clean_columns(csv_file)
    csv_file.to_sql(name=table_name,
                    con=get_datalake_engine(),
                    schema="views",
                    if_exists="replace",
                    index=False)

###############
## Operators ##
###############

class CSVtoPostgresOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            **kwargs):

        self.csv_file = kwargs["csv_file"]
        self.ui_color = job_colors["import"]
        super(CSVtoPostgresOperator, self).__init__(**kwargs)

    def execute(self, context):
        import_csv(self.csv_file, self.task_id)

###################
## Task Builders ##
###################

def build_csv_to_postgres_task(**kwargs):
    task = CSVtoPostgresOperator(
        task_id=kwargs["spec"]["task_id"],
        dag=kwargs["dag"],
        csv_file=kwargs["spec"]["csv_file"]
        )
    return task

####################
## Register Build ##
####################

register_build(build_csv_to_postgres_task)

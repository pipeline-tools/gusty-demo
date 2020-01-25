import json
import datetime
import requests
import pandas as pd

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from .operator_utils.db_connections import get_datalake_engine
from .operator_utils.job_colors import job_colors

from . import register_build

#########
## API ##
#########

def random_joke(**kwargs):
    """
    For getting a random joke and timestamp of the API call from ICNDB API.
    """
    run_timestamp = datetime.datetime.now()
    url = 'http://api.icndb.com/jokes/random?escape=javascript'
    response = requests.get(url).json()["value"]
    fields = {k: [response[k]] for k in ["id", "joke"]}

    df = pd.DataFrame(fields)

    df["timestamp"] = run_timestamp
    df["joke_id"] = df.id
    df = df[["timestamp", "joke_id", "joke"]]

    return df

###############
## Operators ##
###############

class RandomJokeOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            **kwargs):

        self.ui_color = job_colors["import"]
        super(RandomJokeOperator, self).__init__(**kwargs)

    def execute(self, context):
        joke = random_joke()
        joke.to_sql(name=self.task_id,
                    con=get_datalake_engine(),
                    schema="views",
                    if_exists="append",
                    index=False)

###################
## Task Builders ##
###################

def build_random_joke_task(**kwargs):
    task = RandomJokeOperator(
        task_id=kwargs["spec"]["task_id"],
        dag=kwargs["dag"]
        )
    return task

####################
## Register Build ##
####################

register_build(build_random_joke_task)

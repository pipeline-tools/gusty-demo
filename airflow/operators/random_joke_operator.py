import json
import datetime
import requests
import pandas as pd

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook

from sqlalchemy import create_engine

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
    ui_color = "#f5adac"

    @apply_defaults
    def __init__(
            self,
            **kwargs):

        super(RandomJokeOperator, self).__init__(**kwargs)

    def execute(self, context):
        joke = random_joke()
        joke.to_sql(name=self.task_id,
                    con=create_engine(BaseHook.get_connection('postgres_datalake').get_uri()).connect(),
                    schema="views",
                    if_exists="append",
                    index=False)

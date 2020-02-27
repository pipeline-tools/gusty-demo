import json
import datetime
import requests
import pandas as pd

from airflow.utils.decorators import apply_defaults
from airflow.models.baseoperator import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook

##############
## Operator ##
##############

class RandomJokeOperator(BaseOperator):
    ui_color = "#f5adac"

    @apply_defaults
    def __init__(
            self,
            **kwargs):

        super(RandomJokeOperator, self).__init__(**kwargs)

    def execute(self, context):

        # Get a random joke and timestamp of the API call from ICNDB API.
        # Turn it into a pandas dataframe
        run_timestamp = datetime.datetime.now()
        url = 'http://api.icndb.com/jokes/random?escape=javascript'
        response = requests.get(url).json()["value"]
        df = pd.DataFrame({"timestamp": [run_timestamp],
                           "joke_id": [response["id"]],
                           "joke": [response["joke"]]})


        # Get postgres hook
        hook = PostgresHook(postgres_conn_id = 'postgres_default')
        engine = hook.get_sqlalchemy_engine()

        # Send joke to postgres
        df.to_sql(name=self.task_id,
                  con=engine,
                  schema='views',
                  if_exists="append",
                  index=False)

import json
import datetime
import requests
import pandas as pd

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook

from gusty.operators.python_to_postgres_operator import PythonToPostgresOperator

from sqlalchemy import create_engine

###############
## Operators ##
###############

class RandomJokeOperator(PythonToPostgresOperator):
    ui_color = "#f5adac"

    def get_data(self, context):
        # Get a random joke and timestamp of the API call from ICNDB API.
        run_timestamp = datetime.datetime.now()
        url = 'http://api.icndb.com/jokes/random?escape=javascript'
        response = requests.get(url).json()["value"]
        
        df = pd.DataFrame({"timestamp": [run_timestamp],
                           "joke_id": [response["id"]],
                           "joke": [response["joke"]]})

        return df

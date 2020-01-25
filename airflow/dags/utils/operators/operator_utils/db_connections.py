from airflow.models import Variable
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def get_datalake_engine():
    datalake_user = Variable.get('datalake_user')
    datalake_password = Variable.get('datalake_password')
    datalake_host = Variable.get('datalake_host')
    datalake_port = Variable.get('datalake_port')

    datalake_conn_string = ("postgresql://" +
                            datalake_user + ":" +
                            datalake_password + "@" +
                            datalake_host + ":" +
                            datalake_port + "/" +
                            "datalake")

    engine = create_engine(datalake_conn_string)

    return engine

from airflow.hooks.base_hook import BaseHook
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
import sqlalchemy

datalake_conn_string = BaseHook.get_connection('postgres_datalake').get_uri()

engine = create_engine(datalake_conn_string)

# create database
if not database_exists(engine.url):
    create_database(engine.url)

# create schema, give permissions
if not engine.dialect.has_schema(engine, 'views'):
    engine.execute(sqlalchemy.schema.CreateSchema('views'))
    engine.execute("GRANT ALL PRIVILEGES ON DATABASE datalake TO airflow;")
    engine.execute("GRANT ALL PRIVILEGES ON SCHEMA views TO airflow;")
    engine.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA views TO airflow;")

    engine.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA views GRANT ALL PRIVILEGES ON TABLES TO airflow;")

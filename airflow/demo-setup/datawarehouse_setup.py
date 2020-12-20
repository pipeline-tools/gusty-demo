from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy_utils import create_database, database_exists
import sqlalchemy

uri = PostgresHook.get_connection('postgres_default').get_uri()
engine = sqlalchemy.create_engine(uri)

# create database
if not database_exists(engine.url):
    create_database(engine.url)
    engine.execute("GRANT ALL PRIVILEGES ON DATABASE {db} TO {user};".format(user = engine.url.username, db = engine.url.database))

# create schema, give permissions
if not engine.dialect.has_schema(engine, 'views'):
    engine.execute(sqlalchemy.schema.CreateSchema('views'))
    engine.execute("GRANT ALL PRIVILEGES ON SCHEMA views TO {user};".format(user = engine.url.username))
    engine.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA views TO {user};".format(user = engine.url.username))
    engine.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA views GRANT ALL PRIVILEGES ON TABLES TO {user};".format(user = engine.url.username))

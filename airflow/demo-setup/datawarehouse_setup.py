from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy_utils import create_database, database_exists
import sqlalchemy

uri = PostgresHook.get_connection('postgres_default').get_uri()
engine = PostgresHook().get_sqlalchemy_engine()

# create database
if not database_exists(engine.url):
    create_database(engine.url)
    with engine.begin() as conn:
        conn.execute("GRANT ALL PRIVILEGES ON DATABASE {db} TO {user};".format(user = engine.url.username, db = engine.url.database))

# create schema, give permissions
if not engine.dialect.has_schema(engine, 'views'):
    with engine.begin() as conn:
        conn.execute(sqlalchemy.schema.CreateSchema('views'))
        conn.execute("GRANT ALL PRIVILEGES ON SCHEMA views TO {user};".format(user = engine.url.username))
        conn.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA views TO {user};".format(user = engine.url.username))
        conn.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA views GRANT ALL PRIVILEGES ON TABLES TO {user};".format(user = engine.url.username))

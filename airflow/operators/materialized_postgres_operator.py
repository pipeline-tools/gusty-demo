from airflow.utils.decorators import apply_defaults
from airflow.operators.postgres_operator import PostgresOperator
from utils.sql_templates import postgres_create_table, postgres_comment_table
from utils.parsing import detect_dependencies

# postgres_create_table creates table names based on task_id
# So we can parse the sql for tables that postgres_create_table has created
# By defining a list of schemas to cross check against
check_schemas = ['views', 'app', 'another_schema']

class MaterializedPostgresOperator(PostgresOperator):
    ui_color = "#c37ed5"
    template_fields = PostgresOperator.template_fields + ("schema", "description", "fields", )

    @apply_defaults
    def __init__(
            self,
            task_id,
            sql,
            postgres_conn_id = "postgres_default",
            schema = "views",
            description = None,
            fields = None,
            **kwargs):

        self.schema = schema
        self.description = description
        self.fields = fields
        self.check_schemas = check_schemas
        self.check_schemas.append(self.schema)
        self.check_schemas = list(set(self.check_schemas))


        # Turn the SQL into a CREATE TABLE + document command
        # Note that airflow placeholds like {{ds}} still work in your sql yml
        create_sql = postgres_create_table.render(task_id = task_id,
                                                  schema = schema,
                                                  sql = sql)
        doc_sql = postgres_comment_table.render(task_id = task_id,
                                                schema = schema,
                                                description = description,
                                                fields = fields)
        combined_sql = create_sql + "\n" + doc_sql

        # Automatically detect dependencies (gusty will resolve later)
        self.dependencies = detect_dependencies(sql, self.check_schemas)

        super(MaterializedPostgresOperator, self).__init__(
            task_id = task_id,
            sql = combined_sql,
            postgres_conn_id = postgres_conn_id,
            **kwargs)

import os
import re

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from jinja2 import Template

from sqlalchemy import create_engine

from .operator_utils.db_connections import get_datalake_engine
from .operator_utils.job_colors import job_colors

from . import register_build

###############
## Functions ##
###############

def render_query(**kwargs):

    template = Template('''
        -- Create table
        CREATE TABLE views.{{ task_id }}_tmp
        AS ({{ query }});

        -- Drop existing table
        DROP TABLE IF EXISTS views.{{ task_id }};

        -- Replace query
        ALTER TABLE views.{{ task_id }}_tmp RENAME TO {{ task_id }};

        {% if fields %}
        -- Table comments
        {% for field in fields %}
        {% for field_name, field_description in field.items() %}
            COMMENT ON COLUMN views.{{ task_id }}."{{ field_name }}" IS '{{ field_description }}';
        {% endfor %}
        {% endfor %}
        {% endif %}

        -- Commit
        COMMIT;
    ''')

    query = template.render(kwargs)

    return query

###############
## Operators ##
###############

class MaterializedPostgresOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            **kwargs):

        self.query = kwargs["query"]
        self.fields = kwargs["fields"]
        self.ui_color = job_colors["sql"]
        super(MaterializedPostgresOperator, self).__init__(**kwargs)

    def execute(self, context):
        query = render_query(task_id = self.task_id,
                             query = self.query,
                             fields = self.fields)
        print("\n" + query)

        conn = get_datalake_engine().connect()

        try:
            conn.execute(query)
        finally:
            conn.close()

###################
## Task Builders ##
###################

def build_materialized_postgres_operator(**kwargs):
    task = MaterializedPostgresOperator(
        task_id=kwargs["spec"]["task_id"],
        dag=kwargs["dag"],
        query = kwargs["spec"]["query"],
        fields = kwargs["spec"]["fields"] if "fields" in dict(kwargs["spec"]).keys() else None
        )
    return task


####################
## Register Build ##
####################

register_build(build_materialized_postgres_operator)

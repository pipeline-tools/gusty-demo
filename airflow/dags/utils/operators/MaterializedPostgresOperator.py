import os
import re

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook

from jinja2 import Template

from sqlalchemy import create_engine

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

        -- Table description
        {% if description %}
            COMMENT ON TABLE views.{{ task_id }} IS '{{ description | replace("\'", "\'\'") }}';
        {% endif %}

        -- Field descriptions
        {% if fields %}
        {% for field in fields %}
        {% for field_name, field_description in field.items() %}
            COMMENT ON COLUMN views.{{ task_id }}."{{ field_name }}" IS '{{ field_description | replace("\'", "\'\'") }}';
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
        self.description = kwargs["description"]
        self.ui_color = job_colors["sql"]
        super(MaterializedPostgresOperator, self).__init__(**kwargs)

    def execute(self, context):
        query = render_query(task_id = self.task_id,
                             query = self.query,
                             fields = self.fields,
                             description = self.description)
        print("\n" + query)

        conn = create_engine(BaseHook.get_connection('postgres_datalake').get_uri()).connect()

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
        fields = kwargs["spec"]["fields"] if "fields" in dict(kwargs["spec"]).keys() else None,
        description = kwargs["spec"]["description"] if "description" in dict(kwargs["spec"]).keys() else None
        )
    return task


####################
## Register Build ##
####################

register_build(build_materialized_postgres_operator)

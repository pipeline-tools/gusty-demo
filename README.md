# Introduction

The purpose of this repo is to provide a jumping-off point for others to use Airflow to set up their own data pipelines without having to configure Airflow from scratch.

The `ez-airflow` project has a few opinions:

- Data pipelines empower data workers to do three things, two of which `ez-airflow` addresses:

    1. **Ingesting data** - Data is ingested from different sources, through the use of user-defined operators. Ideally, one operator should be built to interface with one data source. This data is then stored in a central data warehouse. Ideally, each data source is stored in its own schema.
    2. **Transforming data** - Once raw data is ingested, it can be manipulated and rendered into **views**. These views are tables generated using a user-defined SQL operator. (In time, it would be nice to build in Python and R operators that could generate views, as well.) These views are stored back into the data warehouse, and it is ideal if these tables are stored in a schema named `views`. (In time, it would be nice to build in export tasks, that could export views to other destinations, like AWS S3.)
    3. **Machine learning** - Once data has been formatted into views and stored, users should be able to run machine learning jobs to create predictive models meant for production needs. `ez-airflow` does not handle this yet.

- The utilities provided in `ez-airflow` should be general enough for anyone to use. It is a foundation upon which individuals can build a data pipeline in Airflow that is suited for their specific needs.

- Jobs are defined using `.yml` files.

- All operators:

    - Are explicitly defined by users, and located in `airflow/dags/utils/operators`.
    - Have their names defined by the `.py` file that contains their interface to Airflow.
    - Use a four-part format:
    
        1. **API** - Defines the functions that will be executed by the operator.
        2. **Operator** - Defines the operator, which is built off of Airflow's BaseOperator, but could probably inheret other operator classes, as well.
        3. **Builder** - Defines a function that builds the and returns the operator.
        4. **Registration** - Registers the builder function to the app. This is done with the `register_build` function.

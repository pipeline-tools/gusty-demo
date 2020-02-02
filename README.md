# Quick Start

Clone this repo to your local machine and get Airflow up and running locally in three easy steps:

### 1: Edit Your Bash Profile

Using your terminal, copy/paste the following into your bash profile:

```
export EZ_AF_USER=airflow
export EZ_AF_PASSWORD=airflowpw
export EZ_AF_R_SERVER=rserver
export EZ_AF_PYTHON_SERVER=pythonserver
export EZ_AF_META_DB=postgresql://${EZ_AF_USER}:${EZ_AF_PASSWORD}@postgres:5432/airflow
export EZ_AF_DATALAKE=postgresql://${EZ_AF_USER}:${EZ_AF_PASSWORD}@postgres:5432/datalake
```

After saving these changes to your bash profile, remember to restart the terminal or open a new one.

### 2: Build with `docker-compose`

While in the ez-airflow directory, run the following command:

```
docker-compose build --build-arg EZ_AF_USER=$EZ_AF_USER --build-arg EZ_AF_PASSWORD=$EZ_AF_PASSWORD
```

If this is your first time building, the build will take several minutes.

### 3: Stand up with `docker-compose`

Finally, while in the ez-airflow directory, simply run:

```
docker-compose up
```

Airflow should be waiting for you at `localhost:8080`!

# Overview

The purpose of this repo is to provide a jumping-off point for others to use Airflow to set up their own data pipelines without having to configure Airflow from scratch.

The `ez-airflow` project has a few opinions:

- Data pipelines empower data workers to do three things, two of which `ez-airflow` addresses:

    1. **Ingesting data** - Data is ingested from different sources, through the use of user-defined operators. Ideally, one operator should be built to interface with one data source. This data is then stored in a central data warehouse. Ideally, each data source is stored in its own schema.
    2. **Transforming data** - Once raw data is ingested, it can be manipulated and rendered into **views**. These views are tables generated using a user-defined SQL operator. (In time, it would be nice to build in Python and R operators that could generate views, as well.) These views are stored back into the data warehouse, and it is ideal if these tables are stored in a schema named `views`. (In time, it would be nice to build in export tasks, that could export views to other destinations, like AWS S3.)
    3. **Machine learning** - Once data has been formatted into views and stored, users should be able to run machine learning jobs to create predictive models meant for production needs. `ez-airflow` does not handle this yet.

- The utilities provided in `ez-airflow` should be general enough for anyone to use. It is a foundation upon which individuals can build a data pipeline in Airflow that is suited for their specific needs.

- Jobs are defined using `.yml` files. For jobs that save to the data warehouse, **the name of the `.yml` file will be the name of the resulting table.**

- All DAGs have two items in the `airflow/dags` folder:

    1. **A `.py` DAG definition file** - This defines the DAG. The DAG's name is determined by the file name.
    2. **A folder for `.yml` job definition files** - The folder should be named the same as its corresponding DAG definition file.

- All operators:

    - Are explicitly defined by users, and located in `airflow/dags/utils/operators`.
    - Have their names defined by the `.py` file that contains their interface to Airflow.
    - Use a four-part format:

        1. **API** - Defines the functions that will be executed by the operator.
        2. **Operator** - Defines the operator, which is built off of Airflow's BaseOperator, but could probably inheret other operator classes, as well.
        3. **Builder** - Defines a function that builds the and returns the operator.
        4. **Registration** - Registers the builder function to the app. This is done with the `register_build` function.

If you are familiar with building Python applications, hopefully you will find this project useful for getting you started with Airflow.

At this point and time, this project is built for PostgreSQL use cases, but in time can grow to include other database usecases.

# Why use `ez-airflow`

The `.yml` approach to generating jobs within Airflow DAGs is not a new idea, but it is useful and there are a few built in benefits to it here.

- **Dependencies** - Dependencies can quickly be set in `.yml` files through one of three means:

    1. Using the `dependencies` specification, you can set dependencies between jobs in the same DAG.
    2. Using the `external_dependencies` specification, you can set dependecies between jobs in different DAGs.
    3. For the `MaterializedPostgresOperator`, dependencies in the same DAG that are a part of the `views` schema are automatically registered.

- **Operator configuration** - After you build an operator, you can pass parameters to it in each `.yml` job definition file. This means that, for example, if you have to call different API endpoints, you may only need to build one operator to ingest data from this API, and then can specify the endpoint to call in the `.yml` job definition file.

- **Support for popular notebook formats** - There are currently two operators, `RmdOperator` and `JupyterOperator`, which enable you to simply write RMarkdown or Jupyter Notebook files and deploy them as jobs in your data pipeline. More importantly, `RmdOperator` and `JupyterOperator` are actually executed on separate dedicated docker containers, and interact with the Airflow container via SSH, which is useful if you want to deploy these services separately in the cloud!

# Setup

## Creating a DAG

In just a few steps, you can create a new dag:

- Copy one of the `.py` files in the `airflow/dags` folder.
- Change the name of the `.py` file to whatever you want your DAG to be called.
- Within the `.py` file, change the `owner` and `email` owners in the `default_args` dict, around lines 20 to 30. (Email notications are currently turned off by default.)
- DAGs are currently set to run once a day. You can change this interval using the `schedule_interval` parameter in the DAG instantiation, around line 35.

Once you've done this, you'll want to create a folder inside of `airflow/dags` for your `.yml` job definition files. Two notes here:

- ***Your folder must be named exactly the same as your DAG definition file. If you DAG is defined in `airflow/dags/my_awesome_dag.py`, then you must have a folder `airflow/dags/my_awesome_dag` to house your `.yml` job definition files.***
- There is a `airflow/dags/csv` folder that does not correspond to a specifc DAG file. This folder is meant to house any .csv files you want to import to your data warehouse. These .csv files can be ingested using the `CSVtoPostgresOperator`, which will be covered later.

## Creating a new job

Using the example above, you now have a definition file, `airflow/dags/my_awesome_dag.py`, and a folder for your jobs, `airflow/dags/my_awesome_dag`. Let's put a job in this DAG.

There is a .csv file we could bring into our warehouse, `airflow/dags/csv/baby_names.csv`. To do this, we will make a new `.yml` job definition file, `airflow/dags/my_awesome_dag/baby_names.yml`. This `.yml` file must include an `operator` parameter, to specify that we will be using the `CSVtoPostgresOperator`, and a `csv_file` parameter to specify the .csv file we will be uploading to our data warehouse:

```yaml
operator: CSVtoPostgresOperator
csv_file: baby_names.csv
```

Now, when the my_awesome_dag DAG runs, it will identify the above job, read the .csv, and upload it to the data warehouse. Neat.

## Creating a new operator

(To Add Later)

# Descriptions of Operators

Now for a quick overview of the two useful general operators that have been built out so far, the `CSVtoPostgresOperator` and the `MaterializedPostgresOperator`.

## CSVtoPostgresOperator

- Required Parameters:

    - **operator** - Specifies the operator we'll be using. Set to `CSVtoPostgresOperator`.
    - **csv_file** - Specifies the file we'll be uploading. Set to the desired csv file located inside the `airflow/dags/csv` folder.

Example file:

```yaml
operator: CSVtoPostgresOperator
csv_file: baby_names.csv
```

## MaterializedPostgresOperator

- Required Parameters:

    - **operator** - Specifies the operator we'll be using. Set to `MaterializedPostgresOperator`.
    - **query** - Specifies the query to be executed. Starts with `|-` so the query can take place over multiple lines.

- Optional Parameters:

    - **fields** - Allows for commenting on columns in the resulting table for documentation purposes. Each entry should start with a hypen (`-`) and follow the format `field_name: field description`.
    - **dependencies** - Specifies job dependencies in the local DAG. Each entry should start with a hypen (`-`) and the job name.
    - **external_dependencies** - Specifies job dependencies in external DAG. Each entry should start with a hypen (`-`) and follow the format `dag_name: job_name`. This will create an external task sensor to wait for a job in the other DAG.

As mentioned, `MaterializedPostgresOperator` jobs will also parse the query to identify any tables that start with `views.`, check if those tables are in the local DAG, and set those dependencies automatically.

Example file:

```yaml
operator: MaterializedPostgresOperator
external_dependencies:
    - my_awesome_dag: baby_names
fields:
    - year_of_birth: "year of child name births"
    - childs_first_name: "first name of the born babies"
    - count: "number of babies born with childs_first_name"
query: |-
    SELECT
        year_of_birth,
        childs_first_name,
        count
    FROM views.baby_names
```

# Specifying Dependencies

As mentioned above, dependencies are identified by three means:

  1. Using the `dependencies` specification, you can set dependencies between jobs in the same DAG.
  2. Using the `external_dependencies` specification, you can set dependecies between jobs in different DAGs.
  3. For the `MaterializedPostgresOperator`, dependencies in the same DAG that are a part of the `views` schema are automatically registered.

## Using `dependencies`

Each entry should start with a hypen (`-`) and the job name.

## Using `external_dependencies`

Each entry should start with a hypen (`-`) and follow the format `dag_name: job_name`. This will create an external task sensor to wait for a job in the other DAG.

Additionally the format `dag_name: all` can be used to specify to wait for an entire DAG to complete before another DAG runs.

## Auto-dependencies in `MaterializedPostgresOperator`

`MaterializedPostgresOperator` jobs will also parse the query to identify any tables that start with `views.`, check if those tables are in the local DAG, and set those dependencies automatically.

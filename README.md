This offers a demo of the [gusty package](https://github.com/chriscardillo/gusty): an opinionated framework for data ETL built on top of [Airflow](https://airflow.apache.org/).

It includes several example DAGs, as well as the Docker infrastructure for you to set up Airflow quickly yourself.

# Quick Start

Clone the repo on your local machine...

```
git clone https://github.com/chriscardillo/gusty-demo.git
```

...and get Airflow up and running locally in three easy steps:


### 1: Edit Your Bash Profile

Using your terminal, copy/paste the following into your bash profile:

```
export GUSTY_USER=gusty
export GUSTY_PASSWORD=rules
```

After saving these changes to your bash profile, remember to restart the terminal or open a new one.

### 2: Build with `docker-compose`

While in the gusty-demo directory, run the following command:

```
docker-compose build --build-arg GUSTY_USER=$GUSTY_USER --build-arg GUSTY_PASSWORD=$GUSTY_PASSWORD
```

If this is your first time building, the build will take several minutes.

### 3: Stand up with `docker-compose`

Finally, while in the gusty-demo directory, simply run:

```
docker-compose up
```

Airflow should be waiting for you at `localhost:8080`!

# Why use gusty

In short, gusty enables users to construct DAGs using YAML. The three big benefits to using gusty are:

## Operator configuration

Airflow's operators, gusty's operators, and any custom operators a user may create are able to be accessed and associated with individual tasks using a YAML spec. Essentially, ever parameter of a specific task can be defined in the YAML spec. This means you never have to define a task manually again.

## Dependency setting

Dependencies can quickly be set in `.yml` files through one of three means:

1. Using the `dependencies` specification, you can set dependencies between jobs in the same DAG.
2. Using the `external_dependencies` specification, you can set dependecies between jobs in different DAGs.
3. For gusty's `MaterializedPostgresOperator`, dependencies in the same DAG that are a part of a `views` schema are automatically registered.

## Notebook support

There are currently two operators, `RmdOperator` and `JupyterOperator`, which enable you to simply write RMarkdown or Jupyter Notebook files and deploy them as jobs in your data pipeline. Notably, `RmdOperator` and `JupyterOperator` are actually executed on separate dedicated docker containers, and interact with the Airflow container via SSH, which is useful if you want to deploy these services separately in the cloud!

# Setup

## Creating a DAG

### DAG definition file

DAG definition files, such as `ingest_example.py` and `transform_example.py` do not contain too much information. If you wanted, you could just copy/paste one of these files, change the filename to what you want your DAG to be called, and be on your way.

- Copy one of the `.py` files in the `airflow/dags` folder and change the name of the `.py` file to whatever you want your DAG to be called.
- Within the `.py` file, change the `owner` and `email` owners in the `default_args` dict, around lines 20 to 30. (Email notications are currently turned off by default.)
- The example DAGs are currently set to run once a day. You can change this interval using the `schedule_interval` parameter in the DAG instantiation, around line 35.
- Note that gusty's `build_dag` function simply needs a path to where the job spec (`.yml`, `.Rmd`, etc.) files are located, and the DAG object itself.

Also note that, by default, gusty's `build_dag` defaults to building [latest only](https://airflow.apache.org/docs/stable/concepts.html#latest-run-only) dags. You can alter this behavior by passing the argument `latest_only=False` to the `build_dag` function.

### Task files folder

Assuming you copy/pasted an existing `.py` DAG defintion file, it will be expected that this `.py` DAG definition file has a corresponding folder of the same name, which contains your job specs. Task files, which will be covered below, are generally `.yml` files that contain parameters that tell gusty what jobs to create.

One important note is that there is a `airflow/dags/csv` folder that does not correspond to a specifc DAG file. This folder is meant to house any .csv files you want to import to your data warehouse. These .csv files can be ingested using gusty's `CSVtoPostgresOperator`, which will be covered later.

## Creating a new job

Let's say you have a `.py` DAG definition file, `airflow/dags/my_awesome_dag.py`, and a folder for your tasks, `airflow/dags/my_awesome_dag`. Let's put a job in this DAG.

There is a .csv file we could bring into our warehouse, `airflow/dags/csv/baby_names.csv`. To do this, we will make a new `.yml` task definition file, `airflow/dags/my_awesome_dag/baby_names.yml`. This `.yml` file must include an `operator` parameter, to specify that we will be using the `CSVtoPostgresOperator`, and a `csv_file` parameter to specify the .csv file we will be uploading to our data warehouse:

```yaml
operator: CSVToPostgresOperator
csv_file: baby_names.csv
```

## Specifying Dependencies

Gusty uses task defintion files to identify dependencies in three ways:

1. Using the `dependencies` specification, you can set dependencies between jobs in the same DAG.
2. Using the `external_dependencies` specification, you can set dependecies between jobs in different DAGs.
3. For gusty's `MaterializedPostgresOperator`, dependencies in the same DAG that are a part of the `views` schema are automatically registered.

### Using `dependencies`

Each entry should start with a hypen (`-`) and the job name.

### Using `external_dependencies`

Each entry should start with a hypen (`-`) and follow the format `dag_name: job_name`. This will create an external task sensor to wait for a job in the other DAG.

Additionally the format `dag_name: all` can be used to specify to wait for an entire DAG to complete before another DAG runs.

### Auto-dependencies in `MaterializedPostgresOperator`

`MaterializedPostgresOperator` jobs will also parse the query to identify any tables that start with `views.`, check if those tables are in the local DAG, and set those dependencies automatically.

Now, when the my_awesome_dag DAG runs, it will identify the above job, read the .csv, and upload it to your data warehouse. Note that the name of your tasks becomes the name of the resulting table in your data warehouse.

## Creating a custom operator

gusty will register any operators located in an `operators` folder in the airflow home directory, in our case `airflow/operators`. These operators can then be included in YAML specs just like any others.

It is imperative that your file name uses `snake_case` and your operator uses `camelCase`.

Conslut [Airflow documentation on creating custom operators](https://airflow.apache.org/docs/stable/howto/custom-operator.html) to generate your own operators.

Note that if you are going to be using new parameters for a custom operator, and your custom operator class inherits from an existing Airflow operator, it is important for your custom operators to include a line like:

```python
template_fields = ParentClass.template_fields + ["additional_field"]
```

You can check out an example custom operator at [airflow/operators/random_joke_operator.py](https://github.com/chriscardillo/gusty-demo/blob/master/airflow/operators/random_joke_operator.py). Note the need for an  explicit `execute` method (as is required according to [Airflow documentation on creating custom operators](https://airflow.apache.org/docs/stable/howto/custom-operator.html)).

# Gusty Operators

Now for a quick overview of gusty's operators.

## CSVToPostgresOperator

- Required Parameters:

    - **operator** - Specifies the operator we'll be using. Set to `CSVToPostgresOperator`.
    - **csv_file** - Specifies the file we'll be uploading. Set to the desired csv file located inside the `airflow/dags/csv` folder.

Example file:

```yaml
operator: CSVToPostgresOperator
csv_file: baby_names.csv
```

You can check out a `CSVToPostgresOperator` at [airflow/dags/ingest_example/baby_names.yml](https://github.com/chriscardillo/gusty-demo/blob/master/airflow/dags/ingest_example/baby_names.yml)

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

You can check out a `MaterializedPostgresOperator` at [airflow/dags/transform_example/five_baby_names.yml](https://github.com/chriscardillo/gusty-demo/blob/master/airflow/dags/transform_example/five_baby_names.yml)

## RmdOperator

To use R in your data pipeline, you can use the `RmdOperator`. This operator assumes that there is an external R server on which to run R tasks. It expects an airflow connection, `rserver_default`, which is an ssh connection string. In this demo, we use a docker container, `rserver` to run R tasks. The connection to the R server is specified in `docker-compose.yml`, under `AIRFLOW_CONN_RSERVER_DEFAULT`.

- Required Parameters:

    - **operator** - Specifies the operator we'll be using. Set to `RmdOperator`.

- Optional Parameters:

    - **dependencies** - Covered above.
    - **external_dependencies** - Covered above.

You can write any R code you want here, so long as your R server supports it. Check out the `rserver` directory for more information the docker image and installing packages.

You can check out an `RmdOperator` at [airflow/dags/transform_example/rmd_example.Rmd](https://github.com/chriscardillo/gusty-demo/blob/master/airflow/dags/transform_example/rmd_example.Rmd)

## JupyterOperator

To use Python in your data pipeline, we'd recommend using gusty's `JupyterOperator`. This operator assumes that there is an external Python server on which to run python tasks. It expects an airflow connection, `pythonserver_default`, which is an ssh connection string. In this demo, we use a docker container, `pythonserver` to run python tasks. The connection to the Python server is specified in `docker-compose.yml`, under `AIRFLOW_CONN_PYTHONSERVER_DEFAULT`.

Note that the JupyterOperator can Jupyter Notebook `.ipynb` (version 4) or any other markdown file format with YAML frontmatter. Here is how to configure your file to have the tasks register properly:

- If using `.ipynb`: Add a YAML markdown chunk to the top of your notebook, then specify required and optional parameters as needed.
- If using another markdown format (e.g. a `.Rmd`): Specify required and optional parameters in the YAML frontmatter portion of the file.

As with all other operators, here are the parameters that are taken:

- Required Parameters:

    - **operator** - Specifies the operator we'll be using. Set to `JupyterOperator`.

- Optional Parameters:

    - **dependencies** - Covered above.
    - **external_dependencies** - Covered above.

You can write any Python code you want here, so long as your Python server supports it. Check out the `pythonserver` directory for more information the docker image and installing packages.

You can check out a `JupyterOperator` using a Jupyter Notebook at [airflow/dags/transform_example/jupyter_example.ipynb](https://github.com/chriscardillo/gusty-demo/blob/master/airflow/dags/transform_example/jupyter_example.ipynb) and a `JupyterOperator` using a different markdown file at [airflow/dags/transform_example/all_markdown_example.Rmd](https://github.com/chriscardillo/gusty-demo/blob/master/airflow/dags/transform_example/all_markdown_example.Rmd)

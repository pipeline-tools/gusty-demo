import os
import yaml
import re

from utils.operators import available_builds
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor

###############################################
################# File System #################
###############################################

################
## Read Files ##
################

valid_extensions = ('.yml')

def get_files(dag_name):
    """
    List all file paths in a dag subdirectory
    """
    dags_dir = os.path.join(os.getenv('AIRFLOW_HOME'), "dags")
    yaml_dir = os.path.join(dags_dir, dag_name)
    files = [os.path.join(yaml_dir, file) for file in os.listdir(yaml_dir) if file.endswith(valid_extensions)]
    assert len(files) > 0, "No files with valid extensions found. Valid extensions are " + valid_extensions
    return files

########################
## Reading in yaml specs
########################

def read_yaml_spec(file):
    """
    Reading in yaml specs
    """
    yaml_file = yaml.load(open(file), Loader=yaml.FullLoader)
    assert "operator" in yaml_file, "No operator specified in yaml spec " + file
    task_id = os.path.splitext(os.path.basename(file))[0]
    yaml_file.pop("task_id", None) # task_id can't exist in the spec
    yaml_file["task_id"] = task_id.lower().strip()
    assert yaml_file["task_id"] != "all", "Task name 'all' is not allowed. Please change your task name."
    return yaml_file

def get_yaml_specs(*args, **kwargs):
    files = files if "files" in kwargs else get_files(kwargs["dag_name"])
    yaml_files = [file for file in files if file.endswith('.yml')]
    assert len(yaml_files) > 0, "No .yml files found."
    specs = [*map(read_yaml_spec, yaml_files)]
    return specs

################################################
################# Dependencies #################
################################################

#####################################
## Different kinds of dependencies ##
#####################################

# yaml spec dependencies

def get_yaml_spec_dependencies(spec):
    """
    Get yaml spec dependencies from a single yaml spec.
    """
    yaml_dependencies = {}
    yaml_dependencies["task_id"] = spec["task_id"]
    yaml_dependencies["dependencies"] = spec["dependencies"] if "dependencies" in spec.keys() else []

    query = spec["query"].lower() if "query" in spec.keys() else None
    if query is not None:
        query = re.sub(re.compile(r'\/\*.*\*\/', re.MULTILINE), "", query)
        query = re.sub("--.*\n", "", query)
        query = re.sub(re.compile(r'[\s]+', re.MULTILINE), " ", query)

        query_views = re.finditer("[^a-z\d_\.](views\.[a-z\d_\.]*)", query)
        query_dependencies = [v for v in set(m.group(1) for m in query_views)
                              if v != spec["task_id"]]
        query_dependencies = [*map(lambda x: re.sub("views\.", "", x), query_dependencies)]

        yaml_dependencies["dependencies"] = yaml_dependencies["dependencies"] + query_dependencies

    else:
        pass

    yaml_dependencies["dependencies"] = [dependency.lower() for dependency in yaml_dependencies["dependencies"]]
    yaml_dependencies["dependencies"] = list(set(yaml_dependencies["dependencies"]))

    return yaml_dependencies

# External Dependencies

def get_spec_external_dependencies(spec):
    external_dependencies = {}
    external_dependencies["task_id"] = spec["task_id"]
    external_dependencies["external_dependencies"] = spec["external_dependencies"] if "external_dependencies" in spec.keys() else None
    return external_dependencies

############################
## Dependency Aggregation ##
############################

def get_dependencies(yaml_specs):
    """
    Aggregating Spec and Query dependencies
    """
    yaml_dependencies = [*map(get_yaml_spec_dependencies, yaml_specs)]
    return yaml_dependencies

def get_external_dependencies(yaml_specs):
    external_dependencies = [*map(get_spec_external_dependencies, yaml_specs)]
    external_dependencies = [external_dependency for external_dependency in external_dependencies if external_dependency["external_dependencies"] is not None]
    return external_dependencies

######################
## Set Dependencies ##
######################

def set_dependencies(yaml_specs, tasks, latest_only=True, **kwargs):

    dependencies = get_dependencies(yaml_specs)
    external_dependencies = get_external_dependencies(yaml_specs)

    if latest_only:
         latest_only_operator = LatestOnlyOperator(task_id='latest_only', dag=kwargs["dag"])

    #external_dependencies
    external_tasks = {}
    tasks_with_external_dependencies = []

    for task in external_dependencies:
        task_id = task["task_id"]
        tasks_with_external_dependencies.append(task_id)
        external_dependencies = task["external_dependencies"]

        for external_dependency in external_dependencies:
            external_dag, external_task = list(external_dependency.items())[0]
            wait_for_whole_dag = external_task == r"all"
            task_name = "wait_for_DAG_" + external_dag if wait_for_whole_dag else "wait_for_" + external_task

            if task_name not in external_tasks.keys():
                if wait_for_whole_dag:
                    wait_for_task = ExternalTaskSensor(dag = kwargs["dag"],
                                                       task_id = task_name,
                                                       external_dag_id=external_dag,
                                                       external_task_id=None,
                                                       poke_interval=20,
                                                       timeout=60,
                                                       retries=25)
                    external_tasks[task_name] = wait_for_task
                else:
                    wait_for_task = ExternalTaskSensor(dag = kwargs["dag"],
                                                       task_id = task_name,
                                                       external_dag_id=external_dag,
                                                       external_task_id=external_task,
                                                       poke_interval=60,
                                                       timeout=60,
                                                       retries=25)
                    external_tasks[task_name] = wait_for_task

                if latest_only:
                    wait_for_task.set_upstream(latest_only_operator)

            tasks[task_id].set_upstream(external_tasks[task_name])

    # local dependencies
    for task in dependencies:
        task_id = task["task_id"]
        spec_dependencies = task["dependencies"]
        valid_dependencies = [spec_dependency for spec_dependency in spec_dependencies if spec_dependency in tasks.keys() and spec_dependency != task_id]

        if len(valid_dependencies) == 0 and latest_only and task_id not in tasks_with_external_dependencies:
            tasks[task_id].set_upstream(latest_only_operator)
        else:
            for spec_dependency in valid_dependencies:
                tasks[task_id].set_upstream(tasks[spec_dependency])



###############################################
################# Build Tasks #################
###############################################

def build_task(spec, dag):
    task_id = spec["task_id"]
    operator = spec["operator"]
    assert operator in available_builds.keys(), "Invalid operator in spec " + task_id + ": " + operator
    build = available_builds[operator]
    task = build(spec=spec, dag=dag)
    return task

def build_tasks(yaml_specs, dag):
    task_dict = {}
    for spec in yaml_specs:
        task_dict[spec["task_id"]] = build_task(spec, dag)
    return task_dict

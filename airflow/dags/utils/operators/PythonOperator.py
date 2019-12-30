from airflow.operators.python_operator import PythonOperator

from . import register_build

#########
## API ##
#########

def hello_mr_dag(name="Dag", **kwargs):
    greeting = "Hello " + name
    print(greeting)
    return greeting

python_callables = {"hello_mr_dag": hello_mr_dag}

###################
## Task Builders ##
###################

def build_python_task(**kwargs):
    assert "python_callable" in kwargs["spec"].keys(), "python_callable not in spec " + kwargs["spec"]["task_id"]
    python_callable_name = kwargs["spec"]["python_callable"]
    assert python_callable_name in python_callables.keys(), "Invalid python callable specified in spec " + kwargs["spec"]["task_id"]
    python_callable = python_callables[python_callable_name]
    op_kwargs = kwargs["spec"]["op_kwargs"] if "op_kwargs" in kwargs["spec"].keys() else None
    task = PythonOperator(
        task_id=kwargs["spec"]["task_id"],
        dag=kwargs["dag"],
        python_callable=python_callable,
        op_kwargs=op_kwargs
    )
    return task

####################
## Register Build ##
####################

register_build(build_python_task)

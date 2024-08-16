from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime,timedelta

default_args={
    'owner':'Juancito2085',
    'retries':5,
    'retry_delay':timedelta(minutes=2)
}

with DAG(
    dag_id='third_dag',
    default_args=default_args,
    description='Mi primer dag',
    start_date=datetime(2024, 8, 16,0),
    schedule_interval='@daily'
) as dag:
    task1=BashOperator(
        task_id='first_task',
        bash_command="echo task1 completed"
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo task2 completed"
    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command="echo task 3 completed"
    )
    #Task dependecies method 1
    #task1.set_downstream(task2)
    #task2.set_downstream(task3)

    #Task dependencies method 2
    #task1>>task2
    #task2>>task3

    #Task dependencies
    task1>>[task2,task3]
from datetime import datetime,timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner':'Juancito2085',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

def saludo():
    print('hola mundo')

with DAG(
    default_args=default_args,
    dag_id='dag_with_python',
    description='dag_with_python',
    start_date=datetime(2024, 8, 16, 0),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='saludo',
        python_callable=saludo
    )

    task1
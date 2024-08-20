from datetime import datetime, timedelta
from functions import *

from airflow.providers.google.cloud.operators.gcs import GoogleCloudStorageCreateBucketOperator
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner':'Juancito2085',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}
    
with DAG(
    default_args=default_args,
    dag_id='dag_with_python',
    description='dag_with_python',
    start_date=datetime(2024, 8, 16, 0),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='create_bucket',
        python_callable=create_bucket
    )

    task2 = PythonOperator(
        task_id='download_file',
        python_callable=download_files
    )

    task1
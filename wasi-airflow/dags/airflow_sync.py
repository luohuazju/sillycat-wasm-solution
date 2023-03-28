# -*- coding: utf-8 -*-
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'sillycat',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['luohuazju@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'airflow_sync',
    default_args=default_args,
    description='Sync the scripts and dags from github to DAG',
    template_searchpath="/home/carl/work/scripts",
    schedule_interval=timedelta(days=1),
)

fetch_files_from_github = BashOperator(
    task_id='fetch_files_from_github',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/ && /usr/bin/git pull origin main ',
    dag=dag,
)

copy_dags_to_directory = BashOperator(
    task_id='copy_dags_to_directory',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/ && cp wasi-airflow/dags/*.py ~/airflow/dags/ ',
    dag=dag,
)

copy_scripts_to_directory = BashOperator(
    task_id='copy_scripts_to_directory',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/ && cp wasi-airflow/scripts/*.sh ~/work/scripts/ ',
    dag=dag,
)

fetch_files_from_github >> copy_dags_to_directory
fetch_files_from_github >> copy_scripts_to_directory

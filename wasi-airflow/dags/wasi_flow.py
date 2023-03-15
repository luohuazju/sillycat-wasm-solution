# -*- coding: utf-8 -*-
"""
###  Run WASI build and Process
"""

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
    'system_shell',
    default_args=default_args,
    description='A simple tutorial DAG',
    template_searchpath="/home/carl/work/scripts",
    schedule_interval=timedelta(days=1),
)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)
t2 = BashOperator(
    task_id='call_echo',
    depends_on_past=False,
    bash_command='echo.sh',
    dag=dag,
)
t1 >> t2
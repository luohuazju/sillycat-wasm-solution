# -*- coding: utf-8 -*-
"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](<https://airflow.apache.org/tutorial.html>)
"""
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
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
    template_searchpath="/opt/airflow/dags/scripts",
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
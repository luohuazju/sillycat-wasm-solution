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
    'wasi_flow',
    default_args=default_args,
    description='Build Runtime, AssemblyScript SDK, Rust SDK and test DAG',
    template_searchpath="/home/carl/work/scripts",
    schedule_interval=timedelta(days=1),
)

fetch_poc_from_github = BashOperator(
    task_id='fetch_poc_from_github',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/ && /usr/bin/git pull origin main ',
    dag=dag,
)

########################################
# Rust App
########################################
prepare_rust_dependency = BashOperator(
    task_id='prepare_rust_dependency',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/wasi-consumer-rust/ && '
                 '/home/carl/.cargo/bin/cargo install -f cargo-wasi ',
    dag=dag,
)

build_app_with_rust = BashOperator(
    task_id='build_app_with_rust',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/wasi-consumer-rust/ && '
                 '/home/carl/.cargo/bin/cargo wasi build ',
    dag=dag,
)

#############################################
# AssemblyScript App
#############################################
prepare_as_dependency = BashOperator(
    task_id='prepare_as_dependency',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/wasi-consumer-as/ && '
                 '~/.nodenv/shims/npm install ',
    dag=dag,
)

build_app_with_as = BashOperator(
    task_id='build_app_with_as',
    depends_on_past=False,
    bash_command='cd /home/carl/work/sillycat-wasm-solution/wasi-consumer-as/ && '
                 '~/.nodenv/shims/npm run build:release ',
    dag=dag,
)


fetch_poc_from_github >> prepare_rust_dependency >> build_app_with_rust
fetch_poc_from_github >> prepare_as_dependency >> build_app_with_as

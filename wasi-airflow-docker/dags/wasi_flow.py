# -*- coding: utf-8 -*-
"""
###  Run WASI build and Process
"""

from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
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
    template_searchpath="/opt/airflow",
    schedule_interval=timedelta(days=1),
)

fetch_poc_from_github = BashOperator(
    task_id='fetch_poc_from_github',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow 
        rm -fr sillycat-wasm-solution
        /usr/bin/git clone https://github.com/luohuazju/sillycat-wasm-solution
        """,
    dag=dag,
)

########################################
# Rust App
########################################
prepare_rust_dependency = BashOperator(
    task_id='prepare_rust_dependency',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-consumer-rust/
        ~/.cargo/bin/cargo install -f cargo-wasi 
        """,
    dag=dag,
)

build_app_with_rust = BashOperator(
    task_id='build_app_with_rust',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-consumer-rust/
        ~/.cargo/bin/cargo wasi build 
        """,
    dag=dag,
)

unittest_app_with_rust = BashOperator(
    task_id='unittest_app_with_rust',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-consumer-rust/
        ~/.cargo/bin/cargo test
        """,
    dag=dag,
)

fetch_poc_from_github >> prepare_rust_dependency >> build_app_with_rust >> unittest_app_with_rust
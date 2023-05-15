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

#############################################
# AssemblyScript App
#############################################
prepare_as_dependency = BashOperator(
    task_id='prepare_as_dependency',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-consumer-as/
        /usr/bin/npm install 
        """,
    dag=dag,
)

build_app_with_as = BashOperator(
    task_id='build_app_with_as',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-consumer-as
        /usr/bin/npm run build:release 
    """,
    dag=dag,
)

unittest_app_with_as = BashOperator(
    task_id='unittest_app_with_as',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-consumer-as
        /usr/bin/npm run test 
    """,
    dag=dag,
)

######################################
# Prepare Runtime to Execute App
######################################

build_runtime = BashOperator(
    task_id='build_runtime',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-impl/
        ~/.cargo/bin/cargo build 
        """,
    dag=dag,
)

unittest_runtime = BashOperator(
    task_id='unittest_runtime',
    depends_on_past=False,
    bash_command="""
        cd /opt/airflow/sillycat-wasm-solution/wasi-impl/
        ~/.cargo/bin/cargo test 
        """,
    dag=dag,
)

test_with_rust_app = BashOperator(
    task_id='test_with_rust_app',
    depends_on_past=False,
    bash_command="""
    cd /opt/airflow/sillycat-wasm-solution/wasi-impl/
    ./target/debug/wasi-impl ../wasi-consumer-rust/target/wasm32-wasi/debug/wasi_consumer_rust.wasm consume_add 1 2 | grep -Ev '3' && exit 1
    exit 0
    """,
    dag=dag,
)

test_with_as_app = BashOperator(
    task_id='test_with_as_app',
    depends_on_past=False,
    bash_command="""
    cd /opt/airflow/sillycat-wasm-solution/wasi-impl/
    ./target/debug/wasi-impl ../wasi-consumer-as/build/wasi-consumer-as.wasm consume_add 1 4 | grep -Ev '5' && exit 1
    exit 0
    """,
    dag=dag,
)


fetch_poc_from_github >> prepare_rust_dependency >> build_app_with_rust >> unittest_app_with_rust
fetch_poc_from_github >> prepare_as_dependency >> build_app_with_as >> unittest_app_with_as
fetch_poc_from_github >> build_runtime >> unittest_runtime >> test_with_rust_app
fetch_poc_from_github >> build_runtime >> unittest_runtime >> test_with_as_app
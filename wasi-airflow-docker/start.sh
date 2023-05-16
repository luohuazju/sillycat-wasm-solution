#!/bin/sh -ex

#start the service
cd /opt/airflow
airflow initdb
airflow scheduler -D &
airflow webserver -p 8080
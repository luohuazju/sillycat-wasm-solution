#!/bin/sh -ex

#start the service
airflow initdb
airflow scheduler -D &
airflow webserver -p 8080
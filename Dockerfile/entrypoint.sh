#!/usr/bin/env bash


# Configure database (assuming it is already setup & reachable)
/usr/local/bin/airflow initdb && \
python3 add_superuser.py && \
/usr/local/bin/supervisord -c /etc/supervisord.conf

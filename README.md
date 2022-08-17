# airflow
Exemplo de uso do Airflow em DataOps

> https://www.youtube.com/watch?v=K9AnJ9_ZAXE
<br> <br>
> https://medium.com/agoda-engineering/orchestrating-airflow-tasks-with-docker-swarm-69b5fb2723a7
<br> <br>
> https://medium.com/analytics-vidhya/setting-up-airflow-to-run-with-docker-swarms-orchestration-b16459cd03a2
<br> <br>
> https://towardsdatascience.com/using-apache-airflow-dockeroperator-with-docker-compose-57d0217c8219
<br> <br>
> https://towardsdatascience.com/data-engineering-basics-of-apache-airflow-build-your-first-pipeline-eefecb7f1bb9
<br> <br>
https://towardsdatascience.com/airflow-sharing-data-between-tasks-7bbaa27eeb1
<br> <br>
https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#communication
<br> <br>
> https://www.projectpro.io/recipes/schedule-dag-file-create-table-and-load-data-into-it-mysql-and-hive-airflow
<br> <br>
> https://www.projectpro.io/recipes/migrate-data-from-mysql-hive-using-airflow

<br> 

Providers:
> https://airflow.apache.org/docs/apache-airflow-providers-apache-hive/2.3.3/_api/airflow/providers/apache/hive/index.html
<br> <br>
> https://github.com/apache/airflow/blob/providers-apache-hive/3.0.0/tests/system/providers/apache/hive/example_twitter_dag.py
<br><br>
> https://github.com/apache/airflow/blob/providers-apache-hive/3.0.0/airflow/providers/apache/hive/transfers/mysql_to_hive.py

<br>

Consumindo dados do Hive via python:

> https://github.com/dropbox/PyHive
<br><br>
> https://github.com/big-data-europe/docker-hive


<br>

Formas de controlar a carga : FULL x DIFERENCIAL:

> https://docs.hevodata.com/data-ingestion/query-modes-for-ingesting-data/

<br>

Executando local:
'''
airflow db init

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

airflow webserver --port 8080

airflow scheduler
'''

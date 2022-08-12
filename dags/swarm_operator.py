import airflow
from airflow import DAG
from airflow.contrib.operators.docker_swarm_operator import DockerSwarmOperator

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': False
}
dag = DAG(
    'docker_swarm_sample',          # DAG ID
    default_args=default_args,
    schedule_interval='15 * * * *', # At 15th minute of every hour
    catchup=False
)

with dag as dag:
    t1 = DockerSwarmOperator(
        api_version='auto',                # Docker API version
        command='/bin/sleep 45',           # Command you want to run in the container
        image='centos:latest',             # The base image to use for running the container
        auto_remove=True,                  # Cleanup the container (and Docker service) once completed
        task_id='sleep_with_swarm',        # Unique task ID required by Airflow
    )

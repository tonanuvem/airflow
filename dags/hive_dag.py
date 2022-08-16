# --------------------------------------------------------------------------------
# Load The Dependencies
# --------------------------------------------------------------------------------
import os
from datetime import date, datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.hive.transfers.mysql_to_hive import MySqlToHiveOperator
MySqlToHiveOperator

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "hive_dag"


@task
def fetch_curso():
    """
    This task should retrieve data. There should be csv output files generated by this task and naming
    convention is direction(from or to)_hive_date.csv
    """


@task
def clean_curso():
    """
    This is a placeholder to clean the files. In this step you can get rid of columns and nulls
    and different parts.
    """


@task
def transform_curso():
    """
    This is a placeholder to analyze and transform data.
    """


@task
def transfer_to_db():
    """
    This is a placeholder to extract summary from Hive data and store it to MySQL.
    """


with DAG(
    dag_id=DAG_ID,
    default_args={
        'owner': 'FIAP',
        'retries': 1,
    },
    schedule_interval="@daily",
    start_date=datetime(2022, 6, 1),
    tags=['exemplo'],
    catchup=False,
) as dag:
    fetch_from_mysql = fetch_curso()
    clean = clean_curso()
    transform = transform_curso()
    #hive_to_mysql = transfer_to_db()

    fetch_from_mysql >> clean >> transform

    # --------------------------------------------------------------------------------
    # The following tasks are generated using for loop. The first task puts the eight
    # csv files to HDFS. The second task loads these files from HDFS to respected Hive
    # tables. These two for loops could be combined into one loop. However, in most cases,
    # you will be running different analysis on your incoming and outgoing tweets,
    # and hence they are kept separated in this example.
    # --------------------------------------------------------------------------------

    from_channels = ['fromTwitter_A', 'fromTwitter_B', 'fromTwitter_C', 'fromTwitter_D']
    to_channels = ['toTwitter_A', 'toTwitter_B', 'toTwitter_C', 'toTwitter_D']
    yesterday = date.today() - timedelta(days=1)
    dt = yesterday.strftime("%Y-%m-%d")
    # define where you want to store the csv file in your local directory
    local_dir = "/tmp/"
    # define the location where you want to store in HDFS
    hdfs_dir = " /tmp/"

    for channel in to_channels:

        file_name = f"to_{channel}_{dt}.csv"

        load_to_hdfs = BashOperator(
            task_id=f"put_{channel}_to_hdfs",
            bash_command=(
                f"HADOOP_USER_NAME=hdfs hadoop fs -put -f {local_dir}{file_name}{hdfs_dir}{channel}/"
            ),
        )

        # [START create_hive]
        load_to_hive = HiveOperator(
            task_id=f"load_{channel}_to_hive",
            hql=(
                f"LOAD DATA INPATH '{hdfs_dir}{channel}/{file_name}'"
                f"INTO TABLE {channel}"
                f"PARTITION(dt='{dt}')"
            ),
        )
        # [END create_hive]

        transform >> load_to_hdfs >> load_to_hive #>> hive_to_mysql

    for channel in from_channels:
        file_name = f"from_{channel}_{dt}.csv"
        load_to_hdfs = BashOperator(
            task_id=f"put_{channel}_to_hdfs",
            bash_command=(
                f"HADOOP_USER_NAME=hdfs hadoop fs -put -f {local_dir}{file_name}{hdfs_dir}{channel}/"
            ),
        )

        load_to_hive = HiveOperator(
            task_id=f"load_{channel}_to_hive",
            hql=(
                f"LOAD DATA INPATH '{hdfs_dir}{channel}/{file_name}' "
                f"INTO TABLE {channel} "
                f"PARTITION(dt='{dt}')"
            ),
        )

        transform >> load_to_hdfs >> load_to_hive #>> hive_to_mysql

    from tests.system.utils.watcher import watcher

    # This test needs watcher in order to properly mark success/failure
    # when "tearDown" task with trigger rule is part of the DAG
    list(dag.tasks) >> watcher()

from tests.system.utils import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)
test_run = get_test_run(dag)

git clone https://github.com/apache/airflow.git
cd airflow/
#cat Dockerfile
docker build -t tonanuvem/airflow:hive --build-arg ADDITIONAL_AIRFLOW_EXTRAS=apache.hive .
docker push tonanuvem/airflow:hive

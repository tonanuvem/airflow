docker build -t tonanuvem/mysql:curso_db -f databases/Dockerfile.mysql.curso .
docker build -t tonanuvem/airflow:etl -f Dockerfile/Dockerfile.tonanuvem.airflow .

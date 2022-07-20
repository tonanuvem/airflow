# Download the docker-compose.yaml file
wget 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Make expected directories and set an expected environment variable
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize the database
docker-compose up airflow-init

# Start up all services
docker-compose up -d

IP=$(curl checkip.amazonaws.com)

echo "Acessar $IP:8080 com username/password: airflow "

docker run -d -p 28080:8088 --name superset apache/superset

# Setup your local admin account

docker exec -it superset_app superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@admin.com \
              --password admin

# Migrate local DB to latest

docker exec -it superset_app superset db upgrade

#Load Examples
# docker exec -it superset_app superset load_examples

# Setup roles

docker exec -it superset_app superset init

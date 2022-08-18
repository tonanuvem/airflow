docker run -d -p 28080:8088 --name superset_app -v "../superset:/app/superset_home/superset" --net local_default apache/superset

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


#Load Dashboards
# docker exec -it superset_app superset import-dashboards -p /app/superset_home/superset/dashboard_aula.zip

# Setup roles

docker exec -it superset_app superset init

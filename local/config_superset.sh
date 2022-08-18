dir=`pwd`; dir="$(dirname "$dir")"; echo $dir;

docker run -d --rm -p 8088:8088 --name superset_app -v "$dir/superset:/app/superset_home/superset" --net local_default apache/superset

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

echo ""
echo ""
echo "Config OK"
IP=$(curl -s checkip.amazonaws.com)
echo ""
echo "URLs do projeto:"
echo ""
echo " - SUPERSET         : http://$IP:8088   (login = admin, password = admin)"
echo ""

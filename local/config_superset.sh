dir=`pwd`; dir="$(dirname "$dir")"; echo $dir;

docker run -d --rm -p 8088:8088 --name superset_app -v "$dir/superset:/app/superset_home/superset" --env SUPERSET_SECRET_KEY=fiap --env WTF_CSRF_ENABLED=False --net local_default apache/superset

# Setup your local admin account

docker exec -it superset_app superset fab create-admin \
              --username fiap \
              --firstname Superset \
              --lastname fiap \
              --email admin@admin.com \
              --password fiap

# Migrate local DB to latest
docker exec -it superset_app superset db upgrade

#Load Examples
# docker exec -it superset_app superset load_examples

# Setup roles
docker exec -it superset_app superset init

echo "Loading Dashboard:"
echo 
docker exec -it superset_app superset import-dashboards -p /app/superset_home/superset/dashboard_ETL.zip -u fiap

echo ""
echo ""
echo "Config OK"
IP=$(curl -s checkip.amazonaws.com)
echo ""
echo "URLs do projeto:"
echo ""
echo " - SUPERSET         : http://$IP:8088   (login = fiap, password = fiap)"
echo ""

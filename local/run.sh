docker-compose up -d
echo ""
echo "Aguardando a configuração."
while [ "$(docker logs local-airflow-1 2>&1 | grep ""Login with username: admin"" | wc -l)" != "1" ]; do
  printf "."
  sleep 1
done
docker exec -ti local-airflow-1 airflow users create --role Admin --username fiap --email fiap --firstname fiap --lastname fiap --password fiap
echo "Config OK"
IP=$(curl -s checkip.amazonaws.com)
echo ""
echo "URLs do projeto: (login = fiap, password = fiap)"
echo ""
echo " - AIRFLOW         : $IP:18080"
echo ""

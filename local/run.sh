docker-compose up -d
echo ""
echo "Aguardando a configuração."
while [ "$(docker logs airflow 2>&1 | grep "Login with username: admin" | wc -l)" != "1" ]; do
  printf "."
  sleep 1
done
docker exec -ti airflow airflow users create --role Admin --username fiap --email fiap --firstname fiap --lastname fiap --password fiap
echo ""
echo ""
echo "Config OK"
IP=$(curl -s checkip.amazonaws.com)
echo ""
echo "URLs do projeto:"
echo ""
echo " - AIRFLOW         : http://$IP:18080   (login = fiap, password = fiap)"
echo ""
echo " - PHPMYADMIN      : http://$IP:8082"
echo ""
echo ""

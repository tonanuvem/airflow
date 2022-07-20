# Liberando a porta no caso de rodar no Cloud9
sudo service mysql stop

docker-compose up -d

#echo ""
#echo "Aguardando a configuração do Debezium CDC (Change Data Capture)."
#while [ "$(docker logs nifi_connect_1 2>&1 | grep "Finished starting connectors and tasks" | wc -l)" != "1" ]; do
#  printf "."
#  sleep 1
#done
echo ""
echo "Config OK"
IP=$(curl -s checkip.amazonaws.com)
echo ""
echo "URLs do projeto:"
echo ""
echo " - PostGres UI    : $IP:8080"
echo " - Mongo UI       : $IP:8081"
echo " - MySQL UI        : $IP:8082"
echo " - Redis UI        : $IP:8083"
echo ""

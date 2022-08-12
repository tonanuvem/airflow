docker stack deploy --compose-file stack.yml etl

sleep 5

echo ""
echo ""

docker stack ps etl --no-trunc

echo "Aguardando 60 seg para verificar novamente:"
echo ""

sleep 60
docker stack ps etl --no-trunc

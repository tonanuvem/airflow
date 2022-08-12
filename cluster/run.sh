docker stack deploy --compose-file stack.yml etl

sleep 5

docker stack ps etl --no-trunc

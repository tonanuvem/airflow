#!/bin/bash

docker-compose stop && docker-compose rm -f && docker volume prune -f && git pull
echo ""
echo "Removendo volumes:"
echo ""
# Lista todos os volumes e remove cada um
docker volume ls -q | grep airflow | while read volume; do
  #echo "Removendo volume: $volume"
  docker volume rm "$volume"
done
echo ""
docker stop jupyter && docker rm jupyter
echo ""
docker stop superset_app && docker rm superset_app

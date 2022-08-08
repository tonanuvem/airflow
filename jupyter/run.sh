#!/bin/bash

echo "Executando Jupyter Notebook para análise e transformação dos dados"

dir=`pwd`; dir="$(dirname "$dir")"; echo $dir;

docker run -it --name jupyter --rm -p 8888:8888 -v "$dir":/home/jovyan/work -d jupyter/datascience-notebook


echo ""
echo "Aguardando a configuração do Jupyter."

while [ "$(docker logs jupyter | grep "http://127.0.0.1:8888/lab?token"| wc -l)" != "1" ]; do
  printf "."
  sleep 1
done

echo ""
echo ""
echo "Senha de Bootstrap:"
echo ""

docker logs jupyter | grep "http://127.0.0.1:8888/lab?token"

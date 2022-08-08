#!/bin/bash

echo "Executando Jupyter Notebook para análise e transformação dos dados"

dir=`pwd`; dir="$(dirname "$dir")"; echo $dir;

#docker run -it --name jupyter --rm -p 8888:8888 -v "$dir":/home/jovyan/work -d jupyter/datascience-notebook

docker run -it --name jupyter --rm -p 8888:8888 j-v "$dir":/home/jovyan/work -d jupyter/datascience-notebook \
    start-notebook.sh --NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$JdAN3fe9J45NvK/EPuGCvA$O/tbxglbwRpOFuBNTYrymAEH6370Q2z+eS1eF4GM6Do'

echo ""
echo "Aguardando a configuração do Jupyter."

#while [ "$(docker logs jupyter | grep "     or http://127.0.0.1:8888/lab?token"| wc -l)" != "1" ]; do
#  printf "."
#  sleep 1
#done

echo ""
echo ""
echo "   Senha: "
echo "my-password"

#docker logs jupyter | grep "     or http://127.0.0.1:8888/lab?token"

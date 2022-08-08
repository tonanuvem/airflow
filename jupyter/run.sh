#!/bin/bash

echo "Executando Jupyter Notebook para análise e transformação dos dados"

dir=`pwd`; dir="$(dirname "$dir")"; echo $dir;

#https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#preparing-a-hashed-password

docker run -it --name jupyter --rm -p 8888:8888 -v "$dir":/home/jovyan/work -v "./curso_transform.ipynb:/home/jovyan/curso_transform.ipynb" -d jupyter/datascience-notebook \
    start-notebook.sh --NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$cIQ7S1OapqyvWzmH636CsA$fh0xOdGwdwv6/cxW5Bqi2mPZuSZlG0zGLwcxl7Ulvac'

echo ""
echo "URL de acesso:"
echo ""
echo http://$(curl -s checkip.amazonaws.com):8888
echo ""
echo "   Senha: admin"


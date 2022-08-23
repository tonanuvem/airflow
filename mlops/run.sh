#!/bin/bash

echo "Executando Jupyter Notebook para MLOps"

dir=`pwd`; dir="$(dirname "$dir")"; echo $dir;

#https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#preparing-a-hashed-password
# jupyter/scipy-notebook
# jupyter/datascience-notebook

docker run -it --name jupyter --rm -p 8888:8888 -v "$dir":/home/jovyan/work -v "$dir/csv/:/home/jovyan/csv" -d jupyter/scipy-notebook \
    start-notebook.sh --NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$cIQ7S1OapqyvWzmH636CsA$fh0xOdGwdwv6/cxW5Bqi2mPZuSZlG0zGLwcxl7Ulvac'

echo ""
echo "URL de acesso:"
echo ""
echo http://$(curl -s checkip.amazonaws.com):8888
echo ""
echo "   Senha: admin"
echo ""

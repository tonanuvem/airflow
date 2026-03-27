#!/bin/sh

docker-compose up -d

echo ""
echo "Aguardando a configuração..."

# espera o airflow subir
while ! docker logs airflow 2>&1 | grep -q "Uvicorn running on"; do
  printf "."
  sleep 2
done
echo " ✅"

echo ""
echo "Airflow iniciado!"

# pega senha do admin dos logs (última ocorrência)
ADMIN_PASS=$(docker logs airflow 2>&1 | grep "Password for user 'admin'" | tail -1 | sed -E "s/.*Password for user 'admin': ([^ ]+).*/\1/")

# pega IP público
IP=$(curl -s checkip.amazonaws.com)

echo ""
echo "========================================"
echo "        AMBIENTE PRONTO 🚀"
echo "========================================"
echo ""
echo "🔐 Airflow:"
echo "   URL      : http://$IP:3080"
echo "   usuário  : admin"
echo "   senha    : $ADMIN_PASS"
echo ""
echo "🛢️ phpMyAdmin:"
echo "   URL      : http://$IP:8082"
echo "   usuário  : admin"
echo "   senha    : admin"
echo ""
echo "========================================"
echo ""

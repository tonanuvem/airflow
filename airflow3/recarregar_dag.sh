#!/bin/bash

DAG_ID="ETL_DW"
CONTAINER="airflow"
TIMEOUT=30
INTERVAL=5

echo "Removendo DAG '$DAG_ID' do Airflow (container: $CONTAINER)..."

docker exec $CONTAINER airflow dags delete $DAG_ID --yes 

echo ""
echo ""
echo "⏳ Aguardando DAG '$DAG_ID' ser carregada no Airflow (container: $CONTAINER)..."

elapsed=0

while true; do
    # 1) verifica se DAG existe (carregada)
    if docker exec -i $CONTAINER airflow dags show "$DAG_ID" > /dev/null 2>&1; then
        
        echo "✅ DAG encontrada!"

        # 2) verifica erro de import (muito importante em DAG quebrada)
        IMPORT_ERRORS=$(docker exec -i $CONTAINER airflow dags list-import-errors)

        if echo "$IMPORT_ERRORS" | grep -q "$DAG_ID"; then
            echo "❌ DAG encontrada, mas com ERRO de import!"
            echo "$IMPORT_ERRORS"
            exit 1
        fi

        echo "🚀 DAG carregada e sem erros!"
        break
    fi

    # timeout
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ Timeout após ${TIMEOUT}s aguardando DAG '$DAG_ID'"
        
        echo "📋 Logs de erro de import:"
        docker exec -i $CONTAINER airflow dags list-import-errors
        
        exit 1
    fi

    echo "⌛ Ainda não disponível... (${elapsed}s)"
    sleep $INTERVAL
    elapsed=$((elapsed + INTERVAL))
done

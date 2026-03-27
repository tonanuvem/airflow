docker exec airflow airflow dags delete ETL_DW --yes 

echo "Aguardando 30 seg, enquanto o Airflow importa de volta a DAG..."
while ! docker exec -i airflow airflow dags show ETL_DW > /dev/null 2>&1; do
  echo "⏳ aguardando +5 seg pela DAG..."
  sleep 5
done

docker exec -i airflow airflow dags list-import-errors | grep ETL_DW && {
  echo "❌ erro na DAG"
  exit 1
}

echo "✅ DAG pronta"

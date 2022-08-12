'''
Neste cenário, vamos migrar dados do MySql para o Hive. 
O operador executa sua consulta no MySQL, armazena o arquivo localmente antes de carregá-lo em uma tabela Hive. 
Quaisquer transformações necessárias podem ser feitas quando os dados forem armazenados localmente. 
O usuário pode lê-lo em um dataframe pandas e executar várias operações de transformação nos dados de acordo com os requisitos do caso de uso. 
'''
# Operador necessario:
# pip3 install apache-airflow-providers-apache-hive

# 
import airflow
from datetime import timedelta
from airflow import DAG
from airflow.providers.apache.hive.transfers.mysql_to_hive import MySqlToHiveOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'fiap',    
    'start_date': airflow.utils.dates.days_ago(2),
    # Se uma tarefa falhar, tentar novamente 3x depois de esperar 1 minuto
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}
    
dag_execute_prep_commands = DAG(
    dag_id='execute_prep_commands',
    default_args=args,
    # schedule_interval='0 0 * * *',
    schedule_interval='@once',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
    description='executando comandos de preparação',
)

mysqlquery = """ 
select * from fiap.curso;
"""

load_mysql_to_hive = MySqlToHiveOperator(
            sql= mysqlquery,
                hive_table='fiap.curso',
                create = True,
                mysql_conn_id = "local_mysql",
                task_id = "load_mysql_to_hive",
            hive_cli_conn_id = "hive_local",
            dag = dag_mysql_to_hive)
            
load_mysql_to_hive

if __name__ == '__main__ ':
  dag_mysql_to_hive.cli()

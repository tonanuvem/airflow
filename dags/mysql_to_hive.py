'''
Neste cenário, vamos migrar dados do MySql para o Hive. 
O operador executa sua consulta no MySQL, armazena o arquivo localmente antes de carregá-lo em uma tabela Hive. 
Quaisquer transformações necessárias podem ser feitas quando os dados forem armazenados localmente. 
O usuário pode lê-lo em um dataframe pandas e executar várias operações de transformação nos dados de acordo com os requisitos do caso de uso. 
'''
# Operador necessario:
# pip3 install apache-airflow-providers-apache-hive


# Etapa 1: Importando módulos: importe as dependências do Python necessárias para o fluxo de trabalho.
import airflow
from datetime import timedelta
from airflow import DAG
from airflow.providers.apache.hive.transfers.mysql_to_hive import MySqlToHiveOperator
from airflow.utils.dates import days_ago

# Etapa 2: argumentos padrão: defina os argumentos padrão e específicos do DAG
default_args = {
    'owner': 'fiap',    
    'start_date': airflow.utils.dates.days_ago(2),
    # Se uma tarefa falhar, tentar novamente 3x depois de esperar 1 minuto
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}
    
# Etapa 3: instanciar um DAG: dê o nome do DAG, configure o agendamento e defina as configurações do DAG
dag_execute_prep_commands = DAG(
    dag_id='execute_prep_commands',
    #default_args=None,
    # schedule_interval='0 0 * * *',
    schedule_interval='@once',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
    description='executando comandos de preparação',
)

# Etapa 4: Definir as tarefas: a próxima etapa é configurar as tarefas que desejam todas as tarefas no fluxo de trabalho.
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
            
# Etapa 5: Configurando Dependências: aqui estamos Configurando as dependências ou a ordem em que as tarefas devem ser executadas.
load_mysql_to_hive
if __name__ == '__main__ ':
  dag_mysql_to_hive.cli()

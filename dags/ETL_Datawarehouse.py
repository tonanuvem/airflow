import os, datetime

from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.providers.apache.hive.operators.hive import HiveOperator

DAG_ID = "ETL_Datawarehouse"
CSV_ID = datetime.date.today().strftime("%Y_%m_%d") # ex: 2022_08_17
CSV_FILE = CSV_ID + "_curso_from_mysql.csv"
CSV_CLEAN = CSV_ID + "_CLEAN" + "curso_from_mysql.csv"
CSV_TRANSFORM = CSV_ID + "_TRANSFORM" + "curso_from_mysql.csv"

# Configurar as tarefas que serão usadas no fluxo de trabalho (DAG).
@task
def extrair_dados():
    """
    Esta tarefa recupera os dados do BD Mysqk. Um arquivo de saída csv é gerado por esta tarefa.
    """
    # pip install pymysql
    # pip install pandas
    # import the modules
    from pymysql import connect
    import pandas.io.sql as sql

    # conecta ao mysql via python
    con=connect(user="admin",password="admin",host="mysqldb",database="fiap")

    # le os dados
    df=sql.read_sql('select * from fiap.curso',con)

    # exportar dados para a próxima task
    print(df.info()) # log
    df.to_csv(CSV_FILE, encoding='utf-8-sig')

@task
def clean_dados():
    """
    Esta é uma tarefa responsável por limpar os dados. Nesta etapa, podemos limpar por ex colunas e dados nulos, formatos de datas invalidas, etc.
    """
    import pandas as pd
    df = pd.read_csv(CSV_FILE)
    
    # 1) eliminar matrículas duplicadas
    df = df.drop_duplicates(subset='MATRICULA', keep="first")

    # 2) resolver o que fazer com os valores nulos da materia 4 : trocar NaN por 0
    df["NOTA_MAT_4"].fillna(0, inplace = True)

    # exportar dados para a próxima task
    print(df.info()) # log
    df.to_csv(CSV_CLEAN, encoding='utf-8-sig')

@task
def transformar_dados():
    """
    Esta é uma tarefa responsável por agregar e transformar dados. Nesta etapa, podemos por ex criar novas colunas.
    """
    import pandas as pd
    df = pd.read_csv(CSV_CLEAN)
    
    # 3) inserir coluna descritiva sobre os alunos que falam ingles, ajustando valores nulos
    import numpy as np
    df["INGLES"].fillna(-1, inplace = True)
    conditions = [df['INGLES'] > 0, df['INGLES'] == 0, df['INGLES'] < 0]
    choices = ['SIM', 'NÃO', 'SEM RESPOSTA'] # COLUNA COM NOVOS VALORES CRIADOS NESSA ETAPA
    df['INGLES_DESC'] = np.select(conditions, choices)

    # 4) eliminar nota ZERO de alunos sem reprovação (ainda não cursaram as matérias 1, 2, 3, 4)
    # APROVADO, NOTA >= 4
    cond1_mat1 = (df['NOTA_MAT_1'] >= 4) & (df['REPROVACOES_MAT_1'] == 0)
    cond1_mat2 = (df['NOTA_MAT_2'] >= 4) & (df['REPROVACOES_MAT_2'] == 0)
    cond1_mat3 = (df['NOTA_MAT_3'] >= 4) & (df['REPROVACOES_MAT_3'] == 0)
    cond1_mat4 = (df['NOTA_MAT_4'] >= 4) & (df['REPROVACOES_MAT_4'] == 0)
    # REPROVADO, NOTA < 4
    cond2_mat1 = (df['NOTA_MAT_1'] < 4) & (df['REPROVACOES_MAT_1'] > 0)
    cond2_mat2 = (df['NOTA_MAT_2'] < 4) & (df['REPROVACOES_MAT_2'] > 0)
    cond2_mat3 = (df['NOTA_MAT_3'] < 4) & (df['REPROVACOES_MAT_3'] > 0)
    cond2_mat4 = (df['NOTA_MAT_4'] < 4) & (df['REPROVACOES_MAT_4'] > 0)
    # AINDA NAO CURSOU : NOTA = 0, SEM REPROVAÇÕES
    cond3_mat1 = (df['NOTA_MAT_1'] == 0) & (df['REPROVACOES_MAT_1'] == 0)
    cond3_mat2 = (df['NOTA_MAT_2'] == 0) & (df['REPROVACOES_MAT_2'] == 0)
    cond3_mat3 = (df['NOTA_MAT_3'] == 0) & (df['REPROVACOES_MAT_3'] == 0)
    cond3_mat4 = (df['NOTA_MAT_4'] == 0) & (df['REPROVACOES_MAT_4'] == 0)
    # CONDICOES:
    conditions_MAT1 = [cond1_mat1, cond2_mat1, cond3_mat1]
    conditions_MAT2 = [cond1_mat2, cond2_mat2, cond3_mat2]
    conditions_MAT3 = [cond1_mat3, cond2_mat3, cond3_mat3]
    conditions_MAT4 = [cond1_mat4, cond2_mat4, cond3_mat4]
    choices = ['APROVADO', 'REPROVADO', 'AINDA NAO CURSOU'] # COLUNA COM NOVOS VALORES CRIADOS NESSA ETAPA
    # CRIANDO NOVAS COLUNAS:
    df['CURSOU_MAT1_DESC'] = np.select(conditions_MAT1, choices)
    df['CURSOU_MAT2_DESC'] = np.select(conditions_MAT2, choices)
    df['CURSOU_MAT3_DESC'] = np.select(conditions_MAT3, choices)
    df['CURSOU_MAT4_DESC'] = np.select(conditions_MAT4, choices)

    # exportar dados para a próxima task
    print(df.info()) # log
    df.to_csv(CSV_TRANSFORM, encoding='utf-8-sig')
    
@task
def carregar_para_dw():
    """
    Esta é uma tarefa responsável por carregar os dados no DW (Hive).
    """
    import pandas as pd
    df = pd.read_csv(CSV_TRANSFORM)

    # carregar dados na ferramenta DW (neste exemplo = postgres)
    from sqlalchemy import create_engine
    postgres = create_engine('postgresql://admin:admin@postgres:5432/datawarehouse')
    df.to_sql('dw', postgres)

# instanciar fluxo do DAG e suas configs
with DAG(
    dag_id=DAG_ID,
    default_args={
        'owner': 'FIAP',
        'retries': 1,
    },
    schedule_interval="@daily",
    start_date=days_ago(1),
    tags=['ETL'],
    catchup=False,
) as dag:
    extrair_dados() >> clean_dados() >> transformar_dados() >> carregar_para_dw()
    
    ''' # outra forma de declarar as operacoes:
    from airflow.operators.python import PythonOperator

    select_from_mysql = = PythonOperator(
        task_id="extrair_dados",
        python_callable=extrair_dados,
    )
    clean = = PythonOperator(
        task_id="clean_dados",
        python_callable=clean_dados,
    )
    transform = = PythonOperator(
        task_id="transformar_dados",
        python_callable=transformar_dados,
    )
    load_to_hive = = PythonOperator(
        task_id="carregar_para_dw",
        python_callable=carregar_para_dw,
    )

    select_from_mysql >> clean >> transform >> load_to_hive
    '''

import os
from datetime import date, datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.hive.transfers.mysql_to_hive import MySqlToHiveOperator
MySqlToHiveOperator

#ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
#DAG_ID = "hive_dag"
#HOME_DIR = "/home/airflow/"
CSV_FILE = "curso_from_mysql.csv"

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

    # connect the mysql with the python
    con=connect(user="admin",password="admin",host="mysqldb",database="fiap")

    # read the data
    df=sql.read_sql('select * from fiap.curso',con)

    # export the data into the excel sheet
    df.to_csv(CSV_FILE, encoding='utf-8-sig')

@task
def clean_dados():
    """
    Esta é uma tarefa responsável por limpar os dados. Nesta etapa, podemos limpar por ex colunas e dados nulos, formatos de datas invalidas, etc.
    """
    df = pd.read_csv(CSV_FILE)
    
    # 1) eliminar matrículas duplicadas
    df = df.drop_duplicates(subset='MATRICULA', keep="first")

    # 3) resolver o que fazer com os valores nulos da materia 4 : trocar NaN por 0
    df["NOTA_MAT_4"].fillna(0, inplace = True)

@task
def transformar_dados():
    """
    Esta é uma tarefa responsável por agregar e transformar dados. Nesta etapa, podemos por ex criar novas colunas.
    """

    # 2) inserir coluna descritiva sobre os alunos que falam ingles, ajustando valores nulos
    import numpy as np
    df["INGLES"].fillna(-1, inplace = True)
    conditions = [df['INGLES'] > 0, df['INGLES'] == 0, df['INGLES'] < 0]
    choices = ['SIM', 'NÃO', 'SEM RESPOSTA']
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
    choices = ['APROVADO', 'REPROVADO', 'AINDA NAO CURSOU']
    # CRIANDO NOVAS COLUNAS:
    df['CURSOU_MAT1_DESC'] = np.select(conditions_MAT1, choices)
    df['CURSOU_MAT2_DESC'] = np.select(conditions_MAT2, choices)
    df['CURSOU_MAT3_DESC'] = np.select(conditions_MAT3, choices)
    df['CURSOU_MAT4_DESC'] = np.select(conditions_MAT4, choices)

@task
def carregar_para_dw():
    """
    Esta é uma tarefa responsável por carregar os dados no DW (Hive).
    """

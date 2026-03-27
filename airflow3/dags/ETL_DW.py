import os
from datetime import datetime
from airflow import DAG
from airflow.decorators import task

DAG_ID = "ETL_DW"

BASE_PATH = "/tmp"

CSV_ID = datetime.now().strftime("%Y_%m_%d")
CSV_FILE = f"{BASE_PATH}/{CSV_ID}_curso_from_mysql.csv"
CSV_CLEAN = f"{BASE_PATH}/{CSV_ID}_CLEAN_curso_from_mysql.csv"
CSV_TRANSFORM = f"{BASE_PATH}/{CSV_ID}_TRANSFORM_curso_from_mysql.csv"


@task
def extrair_dados():
    """
    Extrai dados do MySQL e salva em CSV
    """
    from pymysql import connect
    import pandas.io.sql as sql

    con = connect(
        user="admin",
        password="admin",
        host="mysqldb",
        database="fiap"
    )

    df = sql.read_sql('SELECT * FROM curso', con)

    print(df.info())
    df.to_csv(CSV_FILE, encoding='utf-8-sig', index=False)

    return CSV_FILE


@task
def clean_dados(input_file: str):
    """
    Limpeza dos dados
    """
    import pandas as pd

    df = pd.read_csv(input_file)

    df = df.drop_duplicates(subset='MATRICULA', keep="first")
    df["NOTA_MAT_4"] = df["NOTA_MAT_4"].fillna(0)

    print(df.info())
    df.to_csv(CSV_CLEAN, encoding='utf-8-sig', index=False)

    return CSV_CLEAN


@task
def transformar_dados(input_file: str):
    """
    Transformação dos dados
    """
    import pandas as pd
    import numpy as np

    df = pd.read_csv(input_file)

    df["INGLES"] = df["INGLES"].fillna(-1)
    conditions = [df['INGLES'] > 0, df['INGLES'] == 0, df['INGLES'] < 0]
    choices = ['SIM', 'NÃO', 'SEM RESPOSTA']
    df['INGLES_DESC'] = np.select(conditions, choices)

    # Condições matérias
    def gerar_status(nota, reprova):
        return np.select(
            [
                (nota >= 4) & (reprova == 0),
                (nota < 4) & (reprova > 0),
                (nota == 0) & (reprova == 0)
            ],
            ['APROVADO', 'REPROVADO', 'AINDA NAO CURSOU']
        )

    df['CURSOU_MAT1_DESC'] = gerar_status(df['NOTA_MAT_1'], df['REPROVACOES_MAT_1'])
    df['CURSOU_MAT2_DESC'] = gerar_status(df['NOTA_MAT_2'], df['REPROVACOES_MAT_2'])
    df['CURSOU_MAT3_DESC'] = gerar_status(df['NOTA_MAT_3'], df['REPROVACOES_MAT_3'])
    df['CURSOU_MAT4_DESC'] = gerar_status(df['NOTA_MAT_4'], df['REPROVACOES_MAT_4'])

    print(df.info())
    df.to_csv(CSV_TRANSFORM, encoding='utf-8-sig', index=False)

    return CSV_TRANSFORM


@task
def carregar_para_dw(input_file: str):
    """
    Carrega dados no DW (MySQL)
    """
    import pandas as pd
    from sqlalchemy import create_engine

    df = pd.read_csv(input_file)

    engine = create_engine('mysql+pymysql://admin:admin@mysqldb:3306/fiap')

    print('Salvando dados no DW...')
    df.to_sql('datawarehouse', engine, if_exists='replace', index=False)

    print('Carga concluída com sucesso')


# DAG
with DAG(
    dag_id=DAG_ID,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['ETL'],
) as dag:

    extracao = extrair_dados()
    limpeza = clean_dados(extracao)
    transformacao = transformar_dados(limpeza)
    carga = carregar_para_dw(transformacao)

    extracao >> limpeza >> transformacao >> carga

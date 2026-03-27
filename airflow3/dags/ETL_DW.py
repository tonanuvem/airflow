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

    # conecta ao mysql via python
    con = connect(
        user="admin",
        password="admin",
        host="mysqldb",
        database="fiap"
    )

    # le os dados
    df = sql.read_sql('SELECT * FROM curso', con)

    # exportar dados para a próxima task
    print(df.info())
    df.to_csv(CSV_FILE, encoding='utf-8-sig', index=False)

    return CSV_FILE


@task
def clean_dados(input_file: str):
    """
    Limpeza dos dados
    Nesta etapa, podemos limpar por ex colunas e dados nulos, formatos de datas invalidas, etc.
    """
    import pandas as pd

    df = pd.read_csv(input_file)

    # 1) eliminar matrículas duplicadas
    df = df.drop_duplicates(subset='MATRICULA', keep="first")

    # 2) resolver o que fazer com os valores nulos da materia 4 : trocar NaN por 0
    df["NOTA_MAT_4"] = df["NOTA_MAT_4"].fillna(0)

    # exportar dados para a próxima task
    print(df.info())
    df.to_csv(CSV_CLEAN, encoding='utf-8-sig', index=False)

    return CSV_CLEAN


@task
def transformar_dados(input_file: str):
    """
    Transformação dos dados
    Responsável por agregar e transformar dados: podemos, por ex, criar novas colunas.
    """
    import pandas as pd
    import numpy as np

    df = pd.read_csv(input_file)

    # 3) inserir coluna descritiva sobre os alunos que falam ingles, ajustando valores nulos
    df["INGLES"] = df["INGLES"].fillna(-1)
    conditions = [df['INGLES'] > 0, df['INGLES'] == 0, df['INGLES'] < 0]
    choices = ['SIM', 'NÃO', 'SEM RESPOSTA']
    df['INGLES_DESC'] = np.select(conditions, choices)

    # 4) eliminar nota ZERO de alunos sem reprovação (ainda não cursaram as matérias 1, 2, 3, 4)
    # Condições matérias
    def gerar_status(nota, reprova):
        return np.select(
            [
                (nota == 0) & (reprova == 0),   # 1º opção: NAO CURSOU
                (nota >= 4) & (reprova == 0),   # 2º opção: APROVADO
            ],
            [
                'AINDA NAO CURSOU',
                'APROVADO'
            ],
            default='REPROVADO'                 # 3º opção: REPROVADO
        ).astype(str)
    def gerar_status(nota, reprova):
        # Começa assumindo que todos estão REPROVADOS (caso padrão / default)
        status = pd.Series('REPROVADO', index=nota.index)
        # Sobrescreve para APROVADO quem tem nota >= 4 e nenhuma reprovação
        aprovado = (nota >= 4) & (reprova == 0)
        status[aprovado] = 'APROVADO'
        # Sobrescreve para AINDA NAO CURSOU quem tem nota 0 e nenhuma reprovação
        # (nota 0 com reprovação = REPROVADO, por isso a condição reprova == 0)
        nao_cursou = (nota == 0) & (reprova == 0)
        status[nao_cursou] = 'AINDA NAO CURSOU'
        return status
    df['CURSOU_MAT1_DESC'] = gerar_status(df['NOTA_MAT_1'], df['REPROVACOES_MAT_1'])
    df['CURSOU_MAT2_DESC'] = gerar_status(df['NOTA_MAT_2'], df['REPROVACOES_MAT_2'])
    df['CURSOU_MAT3_DESC'] = gerar_status(df['NOTA_MAT_3'], df['REPROVACOES_MAT_3'])
    df['CURSOU_MAT4_DESC'] = gerar_status(df['NOTA_MAT_4'], df['REPROVACOES_MAT_4'])

    # exportar dados para a próxima task
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


# instanciar fluxo do DAG e suas configs
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

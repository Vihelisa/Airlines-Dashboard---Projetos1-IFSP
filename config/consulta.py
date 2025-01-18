import psycopg2 
import pandas as pd 
import json
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# Função para conectar ao banco de dados 
def connect_to_db(): 
    try: 
        # Conectar ao banco de dados 
        conn = psycopg2.connect( dbname='dashboard', user='admin', password='admin', host='localhost' ) 
        print("Conexão bem-sucedida!") 
        return conn 
    except Exception as e: 
        print(f"Erro ao conectar ao banco de dados: {e}") 
    return None


# Função para obter dados de uma consulta SQL como DataFrame 
def get_data(query): 
    with open('config/login_bd.json') as file: 
        login = json.load(file) 
        try: # Conectar ao banco de dados 
            conn = connect_to_db() 
            if conn is not None: 
                df = pd.read_sql_query(query, conn) 
                conn.close() 
                return df 
            else: return None 
        except Exception as e: 
            print(f"Erro ao executar a consulta: {e}") 
            return None
    


def close_conection(conexao, cursor):
    # Fechar a conexão 
    cursor.close() 
    conexao.close()


def get_query(): 
    with open('config/query.json') as file: 
        query = json.load(file) 
    df_funcionario = get_data(query['funcionario']) 
    df_empresa = get_data(query['empresa']) 
    df_rotas = get_data(query['rotas']) 
    return df_funcionario, df_empresa, df_rotas




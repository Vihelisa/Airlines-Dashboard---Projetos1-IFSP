import psycopg2 
import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker



# Função para conectar ao banco de dados
def connect_to_db(database, user, password, host):
    try:
        # Criar a URI de conexão
        connection_string = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
        # Criar o engine de conexão
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados:\n{e}")
        return None
    

def connect_to_db_leo(database, user, password, host):
    try:
        # Criar a URI de conexão
        connection_string = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
        # Criar o engine de conexão
        engine = create_engine(connection_string)
        SQLSession = sessionmaker(bind=engine)

        return SQLSession  # Retorna apenas o sessionmaker
    except Exception as e:
        print(f"Erro ao conectar! Detalhes: {e}")
        return None

#teste

def get_data(query):
    with open('config/login_bd_leo.json') as file:
        login = json.load(file)
    try:
        # Conectar ao banco de dados 
        engine = connect_to_db(login["database"], login['user'], login['password'], "localhost")
        try: 
            df = pd.read_sql_query(query, engine) 
            return df 
        except SQLAlchemyError as e: 
            print(f"Erro ao executar a consulta: {e}") 
            return None   
    except:
        print(f"Erro ao conectar!")

def get_data_leo(query):
    with open('config/login_bd_leo.json', encoding='utf-8') as file:
        login = json.load(file)
    try:
        # Obter o objeto sessionmaker
        SQLSession = connect_to_db_leo(login["database"], login['user'], login['password'], "localhost")

        if SQLSession is None:
            raise Exception("Não foi possível criar o sessionmaker.")

        # Criar uma sessão e obter o engine associado
        session = SQLSession()
        engine = session.bind  # O `engine` está associado ao sessionmaker

        try:
            # Consultar o banco de dados
            df = pd.read_sql_query(query, engine)
            return df
        except SQLAlchemyError as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        finally:
            session.close()  # Certifique-se de fechar a sessão
    except Exception as e:
        print(f"Erro ao conectar! Detalhes: {e}")
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

def get_query_leo():
    with open('config/query.json') as file:
        query = json.load(file)

    df_funcionario = get_data_leo(query['funcionario'])
    df_empresa = get_data_leo(query['empresa'])
    df_rotas = get_data_leo(query['rotas'])
    return df_funcionario, df_empresa, df_rotas


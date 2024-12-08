import psycopg2 
import json
import pandas as pd


def make_conection(query):
    try:
        with open('loign_bd.json') as file:
            login = json.load(file)
            print(login)

        # Conectar ao banco de dados 
        conexao = psycopg2.connect( 
            host="localhost", 
            user="admin", 
            password="admin", 
            database="dashboard" 
        )
        # Criar um cursor 
        cursor = conexao.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df =  pd.DataFrame(results, columns=columns)
        print("Conexão bem-sucedida!")
    except:
        print(f"Erro ao conectar!")


def close_conection(conexao, cursor):
    # Fechar a conexão 
    cursor.close() 
    conexao.close()


def get_query():
    with open('query.json') as file:
        query = json.load(file)


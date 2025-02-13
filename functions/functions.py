import secrets
import string
import streamlit as st
import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import sessionmaker
from config.consulta import connect_to_db
from sqlalchemy.sql import text
from sqlalchemy import create_engine, Table, MetaData

from config.consulta import *

def bd_conect():
    engine = connect_to_db("dashboard", "postgres", "root", "localhost")
    # Definir o schema da tabela (sem criar, apenas referenciando) 
    metadata = MetaData(bind=engine) 
    db_session = Table('funcionario', metadata, autoload_with=engine)
    return engine, db_session


def create_user(nome, email, senha, empresa_nome, cargo):
    print('Função create user')
    try:
        try:
            engine, db_session = bd_conect()  # Instanciar a sessão
        except:
            print('Deu erro na conexão')

        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256', salt_length=8)
        novo_usuario = {"nome": nome, "email": email, "senha": hashed_password, "empresa_nome": empresa_nome, "cargo": cargo}

        try:
            with engine.connect() as conn: 
                ins = db_session.insert().values(novo_usuario) 
                conn.execute(ins) 
                print("Dados inseridos com sucesso!")
        except:
            print('erro ao inserir os dados')

        # Envolva a consulta SQL com `text()`

        '''db_session.execute(
            text("INSERT INTO funcionario (nome, email, senha, empresa_nome, cargo) VALUES (:nome, :email, :senha, :empresa_nome, :cargo)"),
            {"nome": nome, "email": email, "senha": hashed_password, "empresa_nome": empresa_nome, "cargo": cargo}
        )
        db_session.execute(
            text("UPDATE funcionario SET idempresa = (SELECT e.idempresa FROM empresa AS e WHERE funcionario.empresa_nome = e.sigla) WHERE empresa_nome IN (SELECT sigla  FROM empresa) AND nome = :nome"),
            {"nome": nome}
        )
        db_session.commit()
        db_session.close()  # Sempre fechar a sessão'''
        return True
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False
    

def fetch_user_info(email, senha):
    """Recupera informações do usuário a partir do banco de dados."""
    try:
        df_funcionario, df_empresa, df_rotas = get_query()
        user_true = df_funcionario.loc[(df_funcionario['email'] == email) & (df_funcionario['senha'] == senha)].reset_index()
        if not user_true.empty:
            return user_true
    except:
        st.error("Não foi possível carregar as informações do perfil.")
    

def validate_user(email, password):
    try:
        df_funcionario, df_empresa, df_rotas = get_query()
        user_true = df_funcionario.loc[(df_funcionario['email'] == email) & (df_funcionario['senha'] == password)]
        if not user_true.empty:
            print('existe')
            return True
    except Exception as e:
        return False
    

def atualizar_senha_bd(user_id, nova_senha):
    """Atualiza a senha do usuário no banco de dados."""
    try:
        db_session = bd_conect()  # Instanciar a sessão
        hashed_password = generate_password_hash(nova_senha, method='pbkdf2:sha256', salt_length=8)
        query = text("UPDATE funcionario SET senha = :senha WHERE idfunc = :user_id")
        db_session.execute(query, {"senha": hashed_password, "user_id": user_id})
        db_session.commit()
        db_session.close()
        return True
    except Exception as e:
        print(f"Erro ao atualizar a senha: {e}")
        return False


def load_css(file_name):
    '''
    Função que faz as modificações feitas em css serem carregadas pelo streamlit
    '''
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def change_page(new_page): 
    '''
    Função para mudar de página 
    '''
    st.session_state.page = new_page


def generate_secure_password(length=12):
    '''
    Função que gera senhas automaticamente para novos usuáirios
    '''
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


# Função para enviar email 
def send_email(to_email, password): 
    from_email = "airlinesdashboard@gmail.com" 
    from_password = "gbjlrvqwntnnslnk" 
    msg = MIMEMultipart() 
    msg['From'] = from_email 
    msg['To'] = to_email 
    msg['Subject'] = 'Sua Nova Senha' 
    body = f'Sua nova senha é: {password}' 
    msg.attach(MIMEText(body, 'plain'))
    try: 
        server = smtplib.SMTP('smtp.gmail.com', 587) 
        server.starttls() 
        server.login(from_email, from_password) 
        text = msg.as_string() 
        server.sendmail(from_email, to_email, text)
        server.quit() 
        st.success(f"Solicitação de cadastro enviada com sucesso! Email enviado para {to_email}") 
    except Exception as e: 
        st.error(f"Erro ao enviar email: {e}")

    
def filter_empty_data(select_trafego, select_mes, select_ano):
    if not select_trafego:
        select_trafego = 'Todos'
    if not select_mes:
        select_mes = 'Todos'
    if not select_ano:
        select_ano = 'Todos'
    return select_trafego, select_mes, select_ano



def multiselect_mes_ano_option(df_trafego, select_mes, select_ano):
    if 'Todos' in select_mes and 'Todos' in select_ano:
        print('Todos tem todos selecionados')
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes', 'ano'])
        return df_traf_all_filtered
    
    elif 'Todos' in select_mes and not 'Todos' in select_ano:
        print('apenas o ano é diferente')
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes'])
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        return df_graph
    
    elif not 'Todos' in select_mes and 'Todos' in select_ano:
        print('Apenas o mes é diferente')
        select_mes = [int(item) for item in select_mes]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['ano'])
        df_graph = df_traf_all_filtered[df_traf_all_filtered['mes'].isin(select_mes)]
        return df_graph
    
    else:
        print('O mes e o ano são diferentes')
        select_mes = [int(item) for item in select_mes]
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_graph = df_traf_todos[df_traf_todos['mes'].isin(select_mes)]
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        return df_graph
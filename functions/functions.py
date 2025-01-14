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


SQLSession = connect_to_db_leo("dashboard", "postgres", "root", "localhost")


def bd_conect():
    engine = connect_to_db("dashboard", "postgres", "root", "localhost")
    # Definir o schema da tabela (sem criar, apenas referenciando) 
    metadata = MetaData(bind=engine) 
    db_session = Table('funcionario', metadata, autoload_with=engine)
    return engine, db_session


def create_user(nome, email, senha, empresa_nome, cargo):
    try:
        db_session = SQLSession()  # Instanciar a sessão

        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256', salt_length=8)
        
        # Envolva a consulta SQL com `text()`
        db_session.execute(
            text("INSERT INTO funcionario (nome, email, senha, empresa_nome, cargo) VALUES (:nome, :email, :senha, :empresa_nome, :cargo)"),
            {"nome": nome, "email": email, "senha": hashed_password, "empresa_nome": empresa_nome, "cargo": cargo}
        )
        db_session.execute(
            text("UPDATE funcionario SET id_empresa = (SELECT e.id_empresa FROM empresa AS e WHERE funcionario.empresa_nome = e.sigla) WHERE empresa_nome IN (SELECT sigla  FROM empresa) AND nome = :nome"),
            {"nome": nome}
        )
        db_session.commit()
        db_session.close()  # Sempre fechar a sessão
        return True
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False
    

def fetch_user_info(user_id):
    """Recupera informações do usuário a partir do banco de dados."""
    try:
        db_session = SQLSession()
        query = text("""
            SELECT nome, email, cargo, empresa_nome, id_empresa 
            FROM funcionario 
            WHERE idfunc = :user_id
        """)
        result = db_session.execute(query, {"user_id": user_id}).fetchone()
        db_session.close()

        if result:
            return {
                "nome": result[0],
                "email": result[1],
                "cargo": result[2],
                "empresa": result[3],
                "id_empresa": result[4],
            }
        else:
            return None
    except Exception as e:
        print(f"Erro ao buscar informações do usuário: {e}")
        return None
    

    # Criando função para estilizar as células com base na eficiência
def estilo_eficiencia(val):
    if val == "Péssima":
        return "background-color: red; color: white;"
    elif val == "Ruim":
        return "background-color: yellow; color: black;"
    elif val == "Boa":
        return "background-color: green; color: white;"
    elif val == "Excelente":
        return "background-color: lightgreen; color: black;"
    return ""


def estilo_desgaste(val):
    if val == "Extremo":
        return "background-color: red; color: white;"
    elif val == "Alto":
        return "background-color: yellow; color: black;"
    elif val == "Médio":
        return "background-color: green; color: white;"
    elif val == "Baixo":
        return "background-color: lightgreen; color: black;"
    return ""



def validate_user(email, password):
    try:
        db_session = SQLSession()
        query = text("SELECT idfunc, email, senha FROM funcionario WHERE email = :email")
        result = db_session.execute(query, {"email": email}).fetchone()
        db_session.close()

        if result:
            user_id, stored_email, stored_password = result
            if check_password_hash(stored_password, password):
                # Armazena os dados do usuário na sessão
                st.session_state.user_id = user_id
                st.session_state.user_email = stored_email  
                return True
        return False
    except Exception as e:
        print(f"Erro ao validar usuário: {e}")
        return False
    

def atualizar_senha_bd(user_id, nova_senha):
    """Atualiza a senha do usuário no banco de dados."""
    try:
        db_session = SQLSession()
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
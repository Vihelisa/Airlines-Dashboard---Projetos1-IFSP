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


SQLSession = connect_to_db("dashboard", "postgres", "root", "localhost")


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
            text("UPDATE funcionario SET idempresa = (SELECT e.idempresa FROM empresa AS e WHERE funcionario.empresa_nome = e.sigla) WHERE empresa_nome IN (SELECT sigla  FROM empresa) AND nome = :nome"),
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
            SELECT nome, email, cargo, empresa_nome 
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
            }
        else:
            return None
    except Exception as e:
        print(f"Erro ao buscar informações do usuário: {e}")
        return None


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

    

if __name__ == "__main__":
    email_teste = "testeleo@gmail.com"
    senha_teste = "123"

    if validate_user(email_teste, senha_teste):
        print("Usuário validado com sucesso!")
    else:
        print("Falha na validação do usuário.")
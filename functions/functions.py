import secrets
import string
import streamlit as st
import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart


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
    from_email = "vitoria.elisa@aluno.ifsp.edu.com" 
    from_password = "amobalet23F" 
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

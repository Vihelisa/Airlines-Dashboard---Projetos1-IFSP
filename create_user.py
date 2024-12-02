import streamlit as st 
from functions.functions import *


def load_css(file_name): 
    with open(file_name) as f: 
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

# Carregar o CSS 
load_css("static/cl_style.css")

def create_user_window():
    st.title("Cadastro de Novo Usuário") 

    # Campos de entrada para novo usuário 
    novo_nome = st.text_input("Nome do novo usuário", "") 
    novo_email = st.text_input("Insira o email do novo usuário", "") 

    # Botão de envio do formulário de cadastro 

    if st.button("Enviar solicitação de cadastro de usuário"): 
        if "@gmail.com" in novo_email:
            # Gerar uma senha segura de 12 caracteres
            senha_gerada = generate_secure_password()
            send_email(novo_email, senha_gerada) 
            st.success(novo_email)
            st.success(senha_gerada) 
        else: 
            st.error("Por favor, insira um nome válido e um email válido.")


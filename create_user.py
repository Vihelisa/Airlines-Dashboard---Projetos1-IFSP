import streamlit as st 
from time import sleep
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
    novo_empresa = st.selectbox("Empresa:", ("GLO", "AZU", "TAM"))
    novo_cargo = st.text_input("Cargo:")

    # Botão de envio do formulário de cadastro 

    if st.button("Enviar solicitação de cadastro de usuário"): 
        print('Botão clicado')
        if "@gmail.com" in novo_email:
            # Gerar uma senha segura de 12 caracteres
            senha_gerada = generate_secure_password()
            print('senha gerada')
            if create_user(novo_nome, novo_email, senha_gerada, novo_empresa, novo_cargo):
                send_email(novo_email, senha_gerada)
            else:
                st.error("Erro ao cadastrar usuário!")
        else: 
            st.error("Por favor, insira um nome e/ou email válido.")

    st.button("Voltar a tela de Login", on_click=lambda: change_page('login'))


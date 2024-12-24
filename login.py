import streamlit as st

from create_user import *
from functions.functions import *


def tela_de_login():
    st.title("Airlines Dashboard")

    # Campos de entrada para usuário e senha
    usuario = st.text_input("Usuário de acesso:", "")
    senha = st.text_input("Senha de acesso:", "", type="password")

    if st.button("Entrar"):
        if validate_user(usuario, senha):
            st.success("Login realizado com sucesso!")
            change_page('principal')
        else:
            st.error("Usuário ou senha incorretos!")

    st.button("Quero cadastrar um novo usuário", on_click=lambda: change_page('cadastro'))

import streamlit as st

from create_user import *
from functions.functions import *


def tela_de_login():
    # Conteúdo do aplicativo Streamlit
    st.title("Airlines Dashboard")

    # Campos de entrada para usuário e senha
    usuario = st.text_input("Usuário de acesso:", "user.user@gmail.com")
    senha = st.text_input("Senha de acesso:", "passwoard123", type="password")

    # Botão de login
    if st.button("Entrar"):
        st.success("Login bem-sucedido")

    st.button("Quero cadastrar um novo usuário", on_click=lambda: change_page('cadastro'))
    
import streamlit as st

from create_user import *
from functions.functions import *


def tela_de_login():
    # Conteúdo do aplicativo Streamlit
    st.title("Airlines Dashboard")

     # Verifique se o usuário já fez login
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # Se já estiver logado, redirecionar para a página principal
        change_page('principal')
        st.session_state.page = 'principal'
    else:
        # Caso contrário, exiba o formulário de login
        usuario = st.text_input("Usuário de acesso:", "")
        senha = st.text_input("Senha de acesso:", "", type="password")  
                                                                   
        def on_click_login(): 
            if validate_user(usuario, senha):
                st.session_state.logged_in = True  # Marcar o login como realizado
                if not usuario == None and not senha == None:
                    st.session_state.email = usuario 
                    st.session_state.senha = senha
                change_page('principal')
                st.session_state.page = 'principal'

            else:
                st.error("Usuário ou senha incorretos!")

        
        st.button("Entrar", on_click=on_click_login)

        st.button("Quero cadastrar um novo usuário", on_click=lambda: change_page('cadastro'))

import streamlit as st
from login import *
from create_user import *
from principal import *
from config.consulta import *
from functions.functions import *

# Carregar o CSS
load_css("static/style.css")

# Fazer a conexão com o banco de dados
df_funcionario, df_empresa, df_rotas = get_query()

# Estado inicial para controle da tela ativa
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Controle de navegação dinâmica
if st.session_state.page == 'login':
    tela_de_login()
elif st.session_state.page == 'cadastro':
    create_user_window()
elif st.session_state.page == 'principal':
    tela_principal()

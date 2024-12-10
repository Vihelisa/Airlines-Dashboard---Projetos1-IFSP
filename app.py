import streamlit as st
#from streamlit_antd_components import menu


from login import *
from create_user import *
from principal import *
from config.consulta import *
from functions.functions import *


# Carregar o CSS
load_css("static/style.css")

#fazendo a conexão com o banco de dados
df_funcionario, df_empresa, df_rotas = get_query()
# Estado inicial para controle da tela ativa 
if 'page' not in st.session_state: 
    st.session_state.page = 'login'

#Página de Login
if st.session_state.page == 'login':
    tela_de_login()

#Página de Cadastro
if st.session_state.page == 'cadastro':
    create_user_window()

if st.session_state.page == 'principal':
    tela_principal()
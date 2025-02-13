import streamlit as st
#from streamlit_antd_components import menu
st.set_page_config(layout="wide")


from login import *
from create_user import *
from principal import *
from functions.functions import *



# Carregar o CSS
load_css("static/style.css")


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
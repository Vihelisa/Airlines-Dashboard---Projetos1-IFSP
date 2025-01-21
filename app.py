import streamlit as st
#from streamlit_antd_components import menu
st.set_page_config(layout="wide")
from login import *
from create_user import *
from principal import *
from functions.functions import *
from config.consulta import *
from views.tela_alterar_senha import *



# Carregar o CSS
load_css("static/style.css")


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
elif st.session_state.page == 'perfil':
    tela_perfil_user()
elif st.session_state.page == 'alterar_senha':
    tela_alterar_senha()

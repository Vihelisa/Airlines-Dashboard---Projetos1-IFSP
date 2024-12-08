import streamlit as st
import streamlit_antd_components as sac

from functions.functions import *
from telas.perfil_user import *
from telas.tela_aeroporto import *
from telas.tela_empresa import *
from telas.tela_voos import *


# Opções de navegação 


def tela_principal():
    load_css("static/principal.css")
    
    with st.sidebar:
        selected = sac.tabs( [ 
            sac.TabsItem(label='Perfil do Usuário', icon='user'), 
            sac.TabsItem(label='Aeroporto', icon='compass'), 
            sac.TabsItem(label='Voos', icon='rocket'), 
            sac.TabsItem(label='Empresas', icon='shop')],
            format_func=lambda x: f'{x}', 
            position='left',
            color='None',
            size=22
        )

    if selected == 'Perfil do Usuário':
        tela_perfil_user()
    elif selected == 'Aeroporto':
        tela_aeroporto()
    elif selected == 'Voos':
        tela_voos()
    elif selected == 'Empresas':
        tela_empresa()
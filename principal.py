import streamlit as st
import streamlit_antd_components as sac

from functions.functions import *
from views.perfil_user import *



# Opções de navegação 


def tela_principal():
    load_css("static/principal.css")

    perfil_user = st.Page(
        page='views/perfil_user.py',
        title='Perfil do usuário',
        icon=':material/person:',
        default=True
    )

    analise_trafego = st.Page(
        page='views/analise_trafego.py',
        title='Análise de Tráfego',
        icon=':material/group:'
    )

    analise_receita = st.Page(
        page='views/analise_receita.py',
        title='Análise de Receita',
        icon=':material/whatshot:'
    )
    efic_operac = st.Page(
        page='views/efic_operac.py',
        title='Eficiência Operacional',
        icon=':material/whatshot:'
    )
    analise_rota = st.Page(
        page='views/analise_rota.py',
        title='Análise de Rota',
        icon=':material/whatshot:'
    )
    analise_temporal = st.Page(
        page='views/analise_temporal.py',
        title='Análise de Temporal',
        icon=':material/whatshot:'
    )

    pg = st.navigation(pages=[
        perfil_user, 
        analise_trafego, 
        analise_receita, 
        efic_operac, 
        analise_rota,
        analise_temporal
    ])

    pg.run()
    
    '''with st.sidebar:
        selected = sac.tabs( [ 
            sac.TabsItem(label='Perfil do Usuário', icon='user'), 
            sac.TabsItem(label='Aeroporto', icon='compass'), 
            sac.TabsItem(label='Voos', icon='rocket'), 
            sac.TabsItem(label='Empresa', icon='shop')],
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
        tela_empresa()'''
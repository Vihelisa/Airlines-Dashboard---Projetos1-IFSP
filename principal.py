import streamlit as st
import streamlit_antd_components as sac
from views.perfil_user import *
from config.consulta import *
from functions.functions import *


# Opções de navegação 
# Função para navegar entre as páginas 

def tela_principal():
    load_css("static/principal.css")

    css = """
        <style>
        /* Altere a cor do texto na barra de navegação */
        .st-navigate .css-10trblm { /* Seletor pode variar, ajuste conforme necessário */
            color: #FFFFFF !important;
        }
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Inicializa o estado da navegação
    if "mostrar_navegacao" not in st.session_state:
        st.session_state.mostrar_navegacao = True
        
    if st.session_state.mostrar_navegacao:
        perfil_user = st.Page(
            page='views/perfil_user.py',
            title='Perfil do usuário',
            icon=':material/person:'
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
        analise_desempeho = st.Page(
            page='views/analise_desempenho.py',
            title ='Análise de Desempenho',
            icon=':material/whatshot:'
        )


        pg = st.navigation(pages=[
            perfil_user, 
            analise_trafego, 
            analise_receita, 
            efic_operac, 
            analise_rota,
            analise_temporal,
            analise_desempeho
        ])

        
        pg.run()
    
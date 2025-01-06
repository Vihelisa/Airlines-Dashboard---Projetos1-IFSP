import streamlit as st
import streamlit_antd_components as sac

from config.consulta import *
from functions.functions import *


#fazendo a conexão com o banco de dados
df_funcionario, df_empresa, df_rotas = get_query()

#filtrando a tabela de rotas para apenas a empresa TAM com id 3
df_tam = df_rotas.loc[df_rotas['id_empresa']==3] #Só pq ainda nn tem sistema de login do usuário




# Opções de navegação 

def tela_principal():
    load_css("static/principal.css")

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

    pg = st.navigation(pages=[
        perfil_user, 
        analise_trafego, 
        analise_receita, 
        efic_operac, 
        analise_rota,
        analise_temporal
    ])

    pg.run()
    
import streamlit as st
from st_aggrid import AgGrid


from functions.functions import *
from app import df_rotas, df_tam


def tela_aeroporto():
    st.title("Dashboard sobre os aeroportos")
    df_quant_voos_aeroporto = df_tam.groupby('aeroporto_de_origem_nome').size().reset_index(name='Quantidade de Voos por cidade')
    lista_aeroporto = df_tam['aeroporto_de_origem_nome'].to_list()
    #TABELA
    st.write("Tabela de quantidade de voos por aeroporto.")
    AgGrid(df_quant_voos_aeroporto)

    #Gráfico da quantidade de voos para cada aeroporto
    st.multiselect(lista_aeroporto)
    st.line_chart(df_quant_voos_aeroporto['Quantidade de Voos por cidade'])

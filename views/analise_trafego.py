import streamlit as st
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid

from principal import *


st.write("""
# Análise de Tráfego Aereo
## Volume de Passageiros
Análise do número total de passageiros por rota e período de mês e ano.
""")
#filtrando dataframe para usar na tela
lista = ['mes', 'ano', 'aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'passageiros_pagos', 'passageiros_gratis']
df_trafego = df_tam[lista]
df_traf = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()

#Criando lista de tragetos para o multiselect de tragetos 
lista_aerop_origem = df_traf['aeroporto_de_origem_nome'].to_list()
lista_aerop_destino = df_traf['aeroporto_de_destino_nome'].to_list()
lista_trageto = ['Todos']
for num in range(len(lista_aerop_origem)):
    trageto = f'{lista_aerop_origem[num]} - {lista_aerop_destino[num]}'
    lista_trageto.append(trageto)

#Filtrando e criando lista para o multiselect de mes e ano
df_traf_ano = df_trafego.groupby(['ano']).sum().reset_index()
lista_ano = df_traf_ano['ano'].to_list()
lista_ano.append('Todos')

df_traf_mes = df_trafego.groupby(['mes']).sum().reset_index()
lista_mes = df_traf_mes['mes'].to_list()
lista_mes.append('Todos')


# Definir as colunas 
col1, col2, col3 = st.columns(3)

# Adicionar os widgets multiselect em colunas separadas 
with col1: 
    select_trageto = st.multiselect("Selecione o trageto", lista_trageto)
with col2: 
    select_mes = st.multiselect("Selecione o mês", lista_mes)
with col3: 
    select_ano = st.multiselect("Selecione o ano", lista_ano)

select_trafego, select_mes, select_ano = filter_empty_data(select_trageto, select_mes, select_ano)

if not 'Todos' in select_trageto:
    lista_df_filtrado = []
    nomes_separados = [nome for sublista in select_trageto for nome in sublista.split('-')]
    for num in range(len(nomes_separados)):
        if num%2 == 0:
            origem = nomes_separados[num].strip()
            destino = nomes_separados[num+1].strip()
            df_filtrado = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == origem) & (df_trafego['aeroporto_de_destino_nome'] == destino)]
            lista_df_filtrado.append(df_filtrado)

    # Combinar todos os DataFrames filtrados em um único DataFrame 
    df_filtro_final = pd.concat(lista_df_filtrado).reset_index(drop=True)
    if 'Todos' in select_mes and 'Todos' in select_ano:
        df_traf_todos = df_filtro_final.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes', 'ano'])
        AgGrid(df_traf_all_filtered) #Tabela de valores
    
    elif 'Todos' in select_mes and not 'Todos' in select_ano:
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_filtro_final.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes'])
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        AgGrid(df_graph) #Tabela de valores
    
    elif not 'Todos' in select_mes and 'Todos' in select_ano:
        select_mes = [int(item) for item in select_mes]
        df_traf_todos = df_filtro_final.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['ano'])
        df_graph = df_traf_all_filtered[df_traf_all_filtered['mes'].isin(select_mes)]
        AgGrid(df_graph) #Tabela de valores
    else:
        select_mes = [int(item) for item in select_mes]
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_filtro_final.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_graph = df_traf_todos[df_traf_todos['mes'].isin(select_mes)]
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        AgGrid(df_graph)#Tabela de valores

else:
    if 'Todos' in select_mes and 'Todos' in select_ano:
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes', 'ano'])
        AgGrid(df_traf_all_filtered) #Tabela de valores
    
    elif 'Todos' in select_mes and not 'Todos' in select_ano:
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes'])
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        AgGrid(df_graph) #Tabela de valores
    
    elif not 'Todos' in select_mes and 'Todos' in select_ano:
        select_mes = [int(item) for item in select_mes]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['ano'])
        df_graph = df_traf_all_filtered[df_traf_all_filtered['mes'].isin(select_mes)]
        AgGrid(df_graph) #Tabela de valores
    else:
        select_mes = [int(item) for item in select_mes]
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_graph = df_traf_todos[df_traf_todos['mes'].isin(select_mes)]
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        AgGrid(df_graph)#Tabela de valores
    


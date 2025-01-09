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
df_trafego = df_tam[['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano', 'passageiros_pagos', 'passageiros_gratis']]
df_trafego.loc[:, 'total_passageiros'] = df_trafego['passageiros_pagos'] + df_trafego['passageiros_gratis']

#Criando lista de tragetos para o multiselect de tragetos 
lista_aerop_origem = df_trafego['aeroporto_de_origem_nome'].to_list()
lista_aerop_destino = df_trafego['aeroporto_de_destino_nome'].to_list()
lista_trageto = ['Todos']
for num in range(len(lista_aerop_origem)):
    trageto = f'{lista_aerop_origem[num]} - {lista_aerop_destino[num]}'
    lista_trageto.append(trageto)

#Filtrando e criando lista para o multiselect de mes e ano
df_traf_ano = df_trafego.groupby(['ano']).sum().reset_index()
lista_ano = df_traf_ano['ano'].to_list()
lista_ano.append('Todos')


# Definir as colunas 
col1, col2 = st.columns(2)

# Adicionar os widgets multiselect em colunas separadas 
with col1: 
    select_trageto = st.multiselect("Selecione o trajeto", lista_trageto)
with col2: 
    select_ano = st.multiselect("Selecione o ano", lista_ano)

select_trafego, select_ano = filter_empty_data(select_trageto, select_ano)

if 'Todos' in select_trageto:
    if 'Todos' in select_ano:
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes', 'ano'])
        print('mostrar tabela')
        st.dataframe(df_traf_all_filtered)

    else:
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes'])
        df_traf_all_filtered = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        st.dataframe(df_traf_all_filtered)
elif len(select_trageto) > 0:
    lista_df_filtrado = []
    nomes_separados = [nome for sublista in select_trageto for nome in sublista.split('-')]
    for num in range(len(nomes_separados)):
        if num%2 == 0:
            origem = nomes_separados[num].strip()
            destino = nomes_separados[num+1].strip()
            df_filtrado = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == origem) & (df_trafego['aeroporto_de_destino_nome'] == destino)]
            lista_df_filtrado.append(df_filtrado)

    df_filtro_final = pd.concat(lista_df_filtrado).reset_index(drop=True)
    # Ordenar o DataFrame pela coluna desejada (substitua 'nome_da_coluna' pelo nome da coluna que você quer usar) 
    df_ordenado = df_filtro_final.sort_values(by='mes', ascending=True)
    if 'Todos' in select_ano:
        df_traf_todos = df_ordenado.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes', 'ano'])
        st.dataframe(df_traf_all_filtered)
    else:
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_ordenado.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano', 'mes']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        st.dataframe(df_traf_all_filtered)
    
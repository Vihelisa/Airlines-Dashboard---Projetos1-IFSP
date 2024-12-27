import streamlit as st

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



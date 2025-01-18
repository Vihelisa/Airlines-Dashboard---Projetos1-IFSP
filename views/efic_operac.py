import streamlit as st

from principal import df_rotas, df_tam

import streamlit as st
import pandas as pd
from config.consulta import *
from functions.functions import fetch_user_info
import plotly.express as px
from principal import df_tam
from functions.functions import *


df_tam = df_rotas

st.title("Análise de Eficiência Operacional")



# Filtrando e renomeando as colunas necessárias
colunas_necessarias = {
    'aeroporto_de_origem_nome': 'Nome Origem',
    'aeroporto_de_origem_uf': 'UF Origem',
    'aeroporto_de_origem_pais': 'País Origem',
    'aeroporto_de_destino_nome': 'Nome Destino',
    'aeroporto_de_destino_uf': 'UF Destino',
    'aeroporto_de_destino_pais': 'País Destino',
    'mes': 'Mês',
    'ano': 'Ano',
    'total_passageiros': 'Total Passageiros',
    'assentos': 'Assentos Disponíveis',
    'assentos_vazios': 'Assentos Vazios',
    'porcentagem': '% Ocupação',
    'resultado_ocupacao': 'Eficiência',
    'plano_de_acao': 'Plano de Ação'
}

# Garantindo que todas as colunas existam no DataFrame
for coluna in colunas_necessarias.keys():
    if coluna not in df_rotas.columns:
        df_rotas[coluna] = None  # Cria a coluna com valores nulos

# Removendo linhas onde o número de assentos disponíveis não está preenchido ou é zero
df_rotas = df_rotas[df_rotas['assentos'].notna() & (df_rotas['assentos'] > 0)]

# Preenchendo o valor de 'Total Passageiros' com a soma de 'Passageiros Pagos' e 'Passageiros Grátis'
if 'passageiros_pagos' in df_rotas.columns and 'passageiros_gratis' in df_rotas.columns:
    df_rotas['total_passageiros'] = df_rotas['passageiros_pagos'].fillna(0) + df_rotas['passageiros_gratis'].fillna(0)

df_rotas['assentos_vazios'] = df_rotas['assentos'].fillna(0) - df_rotas['total_passageiros'].fillna(0)

df_rotas = df_rotas[df_rotas['total_passageiros'] <= df_rotas['assentos']]

# Calculando a porcentagem de ocupação
df_rotas['porcentagem'] = (
    df_rotas['total_passageiros'].fillna(0) / df_rotas['assentos']
) * 100

# Formatando a porcentagem como string com símbolo '%'
df_rotas['porcentagem'] = df_rotas['porcentagem'].apply(lambda x: "{:.1f}%".format(x))

# Formatando a coluna 'Assentos Disponíveis' como inteiro
df_rotas['assentos'] = df_rotas['assentos'].astype(int)

df_rotas['assentos_vazios'] = df_rotas['assentos_vazios'].astype(int)


# Preenchendo a coluna de resultado da ocupação
def classificar_ocupacao(valor):
    if pd.isna(valor):
        return None
    elif valor <= 25:
        return "Péssima"
    elif valor <= 50:
        return "Ruim"
    elif valor <= 75:
        return "Boa"
    else:
        return "Excelente"

df_rotas['resultado_ocupacao'] = df_rotas['porcentagem'].str.rstrip('%').astype(float).apply(classificar_ocupacao)

# Criando função para estilizar as células com base na eficiência
def estilo_eficiencia(val):
    if val == "Péssima":
        return "background-color: red; color: white;"
    elif val == "Ruim":
        return "background-color: yellow; color: black;"
    elif val == "Boa":
        return "background-color: green; color: white;"
    elif val == "Excelente":
        return "background-color: lightgreen; color: black;"
    return ""

# Criando os filtros lado a lado
st.subheader("Filtros")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    filtro_origem = st.selectbox("Origem", 
                                    options=["Todos"] + list(df_rotas['aeroporto_de_origem_nome'].dropna().unique()))
with col2:
    filtro_destino = st.selectbox("Destino", 
                                    options=["Todos"] + list(df_rotas['aeroporto_de_destino_nome'].dropna().unique()))
with col4:
    filtro_ano = st.selectbox("Ano", 
                                options=["Todos"] + sorted(df_rotas['ano'].dropna().unique()))
with col3:
    filtro_mes = st.selectbox("Mês", 
                                        options=["Todos"] + sorted(df_rotas['mes'].dropna().unique()))   
with col5:
    filtro_eficiencia = st.selectbox("Eficiência", 
                                        options=["Todos", "Ruim", "Média", "Boa", "Excelente"])


# Aplicando os filtros ao DataFrame
if filtro_origem != "Todos":
    df_rotas = df_rotas[df_rotas['aeroporto_de_origem_nome'] == filtro_origem]
if filtro_destino != "Todos":
    df_rotas = df_rotas[df_rotas['aeroporto_de_destino_nome'] == filtro_destino]
if filtro_ano != "Todos":
    df_rotas = df_rotas[df_rotas['ano'] == filtro_ano]
if filtro_eficiencia != "Todos":
    df_rotas = df_rotas[df_rotas['resultado_ocupacao'] == filtro_eficiencia]
if filtro_mes != "Todos":
    df_rotas = df_rotas[df_rotas['mes'] == filtro_mes]

df_rotas['plano_de_acao'] = df_rotas['resultado_ocupacao'].apply(gerar_plano_acao_eficiencia)

# Filtrando e renomeando as colunas
df_tabela = df_rotas[list(colunas_necessarias.keys())].rename(columns=colunas_necessarias)

# Exibindo a tabela no Streamlit com estilos
st.subheader("Tabela de Dados Operacionais")
styled_table = df_tabela.style.applymap(estilo_eficiencia, subset=['Eficiência'])
st.dataframe(styled_table, use_container_width=True)



# Verificar se o DataFrame filtrado não está vazio
if not df_rotas.empty:
# Garantir que a coluna 'porcentagem' esteja no formato numérico, tratando erros
    df_rotas['porcentagem'] = (
        df_rotas['porcentagem']
        .str.rstrip('%')  # Remove o símbolo '%' do final
        .apply(pd.to_numeric, errors='coerce')  # Converte para float, definindo NaN para valores inválidos
)

# Remover linhas com valores inválidos na coluna 'porcentagem'
    df_rotas = df_rotas.dropna(subset=['porcentagem'])

# Identificar o top destinos com maior eficiência operacional
    top_destinos = (
        df_rotas.groupby('aeroporto_de_destino_nome', as_index=False)
        .agg({'porcentagem': 'mean'})
        .sort_values(by='porcentagem', ascending=False)
        .head(5)
)

# Verificar se existem dados suficientes para criar o gráfico
    if not top_destinos.empty:
    # Criar o gráfico de barras
        fig = px.bar(
            top_destinos,
            x='aeroporto_de_destino_nome',
            y='porcentagem',
            title='Destinos com Maior Eficiência Operacional',
            labels={'aeroporto_de_destino_nome': 'Destino', 'porcentagem': 'Eficiência (%)'},
            text='porcentagem'
    )

    # Formatar os valores do eixo y como porcentagem
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_tickformat=".1f%%", xaxis_title="Destino", yaxis_title="Eficiência (%)")

    # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não há dados suficientes para exibir o gráfico de Top Destinos.")


    # Identificar o top destinos com maior eficiência operacional
    bot_destinos = (
        df_rotas.groupby('aeroporto_de_destino_nome', as_index=False)
        .agg({'porcentagem': 'mean'})
        .sort_values(by='porcentagem', ascending=True)
        .head(5)
)

# Verificar se existem dados suficientes para criar o gráfico
    if not bot_destinos.empty:
    # Criar o gráfico de barras
        fig = px.bar(
            bot_destinos,
            x='aeroporto_de_destino_nome',
            y='porcentagem',
            title='Destinos com Menor Eficiência Operacional',
            labels={'aeroporto_de_destino_nome': 'Destino', 'porcentagem': 'Eficiência (%)'},
            text='porcentagem',
            color='porcentagem'
    )

    # Formatar os valores do eixo y como porcentagem
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', marker_color='#7c1b07')
        fig.update_layout(yaxis_tickformat=".1f%%", xaxis_title="Destino", yaxis_title="Eficiência (%)")

    # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não há dados suficientes para exibir o gráfico de Bot Destinos.")
else:
    st.warning("Nenhum dado disponível após os filtros para análise gráfica.")



st.write("""
# Eficiência Operacional
## Taxa de Ocupação
Porcentagem de assentos ocupados em cada voo, ajudando a identificar voos com baixa demanda.
""")


st.write("""
## Decolagens e Pousos
Monitoramento do número de decolagens e pousos para otimização do uso das aeronaves.
""")


# Obtendo as informações do usuário logado
#user_info = fetch_user_info(st.session_state.user_id)


'''if not user_info or "id_empresa" not in user_info:
    st.error("Não foi possível obter as informações do usuário logado.")
    return'''

#id_empresa_logado = user_info["id_empresa"]

'''# Obtendo os dados da consulta
_, _, df_rotas = get_query_leo()

# Verificando se os dados foram carregados corretamente
if df_rotas is None or df_rotas.empty:
    st.error("Não foi possível carregar os dados das rotas.")
    return

# Filtrando os dados pela empresa do funcionário logado
if "id_empresa" in df_rotas.columns:
    df_rotas = df_rotas[df_rotas['id_empresa'] == id_empresa_logado]
else:
    st.error("A coluna 'id_empresa' não foi encontrada no DataFrame.")
    return'''
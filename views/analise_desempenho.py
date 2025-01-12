import streamlit as st
import pandas as pd
from config.consulta import get_query_leo
from functions.functions import fetch_user_info
import altair as alt


def tela_analise_desempenho():
    st.title("Análise de Desempenho")

    # Obtendo as informações do usuário logado
    user_info = fetch_user_info(st.session_state.user_id)

    if not user_info or "id_empresa" not in user_info:
        st.error("Não foi possível obter as informações do usuário logado.")
        return

    id_empresa_logado = user_info["id_empresa"]

    # Obtendo os dados da consulta
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
        return

    # Verificando a existência das colunas necessárias
    colunas_necessarias = {'aeroporto_de_origem_nome',
                           'aeroporto_de_destino_nome',
                           'ano',
                           'mes',
                           'decolagens',
                           'distancia_voada_km',
                           'horas_voadas'}
    for coluna in colunas_necessarias:
        if coluna not in df_rotas.columns:
            st.error(f"A coluna '{coluna}' não foi encontrada no DataFrame.")
            return

    # Criando a coluna "Rota"
    df_rotas['Rota'] = df_rotas['aeroporto_de_origem_nome'] + " -> " + df_rotas['aeroporto_de_destino_nome']

    # Agrupando os dados por Rota e Ano, somando os valores relevantes
    df_agrupado = (
        df_rotas.groupby(['Rota', 'ano'], as_index=False)
        .agg({
            'decolagens': 'sum',
            'distancia_voada_km': 'sum',
            'horas_voadas': 'sum'
        })
        .rename(columns={
            'ano': 'Ano',
            'decolagens': 'Voos',
            'horas_voadas': 'Total de Horas Voadas',
            'distancia_voada_km': 'Distância Voada Total (Km)'
        })
    )

    # Definindo a função para classificar o nível de desgaste
    def classificar_desgaste(horas):
        if horas <= 400:
            return "Baixo"
        elif horas <= 700:
            return "Médio"
        elif horas <= 1000:
            return "Alto"
        else:
            return "Extremo"

    df_agrupado['Nível de Desgaste'] = df_agrupado['Total de Horas Voadas'].apply(classificar_desgaste)

    # Filtros
    st.subheader("Filtros")
    col1, col2 = st.columns(2)

    with col1:
        filtro_rota = st.selectbox("Rota", options=["Todas"] + list(df_agrupado['Rota'].unique()))
    with col2:
        filtro_ano = st.selectbox("Ano", options=["Todos"] + sorted(df_agrupado['Ano'].unique()))

    # Aplicando filtros
    df_filtrado = df_agrupado.copy()

    if filtro_rota != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Rota'] == filtro_rota]
    if filtro_ano != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Ano'] == filtro_ano]

    # Exibindo tabela filtrada
    st.subheader("Tabela de Dados de Desempenho")
    if not df_filtrado.empty:
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("Não há dados disponíveis para os filtros selecionados.")
        return

    # Identificando a rota com maior número de horas voadas
    rota_top = df_filtrado.loc[df_filtrado['Total de Horas Voadas'].idxmax()]['Rota']

    # Filtrando o DataFrame original para a rota selecionada
    origem, destino = rota_top.split(" -> ")
    df_mensal = df_rotas[(df_rotas['aeroporto_de_origem_nome'] == origem) &
                         (df_rotas['aeroporto_de_destino_nome'] == destino)]


# Criando a coluna "Mes.Ano"
    df_mensal['MesAno'] = df_mensal['mes'].astype(str).str.zfill(2) + "-" + df_mensal['ano'].astype(str)

# Exibindo o DataFrame mensal para verificar os dados
    st.subheader("Dados Mensais Originais")
    st.dataframe(df_mensal, use_container_width=True)

# Selecionando as colunas relevantes diretamente de df_mensal
    df_mensal_filtrado = df_mensal[['MesAno', 'horas_voadas']].copy()

# Ordenando pelo total de horas voadas e selecionando o Top 5
    df_top5 = df_mensal_filtrado.sort_values(by='horas_voadas', ascending=False).head(5)

# Criando o gráfico com Altair
    chart = (
        alt.Chart(df_top5)
        .mark_bar()
        .encode(
            x=alt.X('MesAno:N', sort=None, title='MêsAno'),  # Garantindo que o eixo X seja categórico
            y=alt.Y('horas_voadas:Q', title='Horas Voadas'),
            tooltip=['MesAno', 'horas_voadas']
    )
        .properties(
            title=f"Top 5 Meses com Maior Número de Horas Voadas",
            width=600,
            height=400
    )
    )

# Exibindo o gráfico no Streamlit
    st.altair_chart(chart, use_container_width=True)


# Chamando a função para exibir a tela
tela_analise_desempenho()

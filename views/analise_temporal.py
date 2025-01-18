import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
import matplotlib.pyplot as plt
import plotly.express as px

from principal import df_rotas, df_tam


st.write("""
# Análise Temporal
## Padrões Sazonais
Identificação de variações sazonais na demanda de passageiros e ajuste da oferta de voos de acordo.
""")
st.write("""Esta avaliação mostra a porcentagem de procura de cada trimente comparando todos os trimestres de todos os anos datados na base de dados e também o trajeto mais procurado para cada trimestre""")
lista = [
    'aeroporto_de_origem_nome', 
    'aeroporto_de_destino_nome', 
    'mes', 
    'ano', 
    'passageiros_pagos', 
    'passageiros_gratis',
]
df_sazonal = df_tam[lista]
df_sazonal_sem_groupby = df_tam[lista]



# Supondo que o DataFrame se chama df
# Criar colunas de ano e trimestre
df_sazonal['mes'] = pd.to_datetime(df_sazonal['mes'], format='%m')  # Certificar-se de que a coluna 'mes' está no formato correto
df_sazonal['trimestre'] = df_sazonal['mes'].dt.quarter

# Calcular a procura total em cada trimestre (todos os anos)
df_sazonal['passageiros_total'] = df_sazonal['passageiros_pagos'] + df_sazonal['passageiros_gratis']
trimestre_total = df_sazonal.groupby('trimestre')['passageiros_total'].sum().reset_index()


# Calcular a procura total anual
total_anual = df_sazonal['passageiros_total'].sum()

# Calcular a porcentagem de procura por trimestre
trimestre_total['procura_porcentagem'] = (trimestre_total['passageiros_total'] / total_anual) * 100

# Encontrar a linha com o maior valor na coluna 'passageiros_total' 
indice_maior_valor = trimestre_total['procura_porcentagem'].idxmax()
indice_menor_valor = trimestre_total['procura_porcentagem'].idxmin()

trimestre_total['possiveis_otimizacoes'] = '' 
trimestre_total.loc[indice_maior_valor, 'possiveis_otimizacoes'] = f"""
Este é o semestre de maior procura durante o ano,
focar em oferecer mais opções de voos e ter maior atenção na frota de aeronaves,
seja aumentando a frota ou oferecendo mais manutenções
"""
trimestre_total.loc[indice_menor_valor, 'possiveis_otimizacoes'] = 'Este é o semestre de menor procura durante o ano, focar em oferecer promoções durante o semestre e pensar em uma boa logistica para não usar aeronaves que serão importantes para outros momentos de maior fluxo de passageiros'
# Aplicar estilos ao DataFrame 
st.write(f""" 
        <div style="height:325px;overflow-y:scroll;"> 
            {trimestre_total.to_html(escape=False)} 
        """, unsafe_allow_html=True
)

fig = px.pie(trimestre_total, values='procura_porcentagem', names='trimestre', title='Porcentagem de cada trimestre') 
# Exibir o gráfico
st.plotly_chart(fig)

# Encontrar o trajeto mais procurado em cada trimestre (todos os anos)
trajeto_mais_procurado = df_sazonal.groupby(['trimestre', 'aeroporto_de_origem_nome', 'aeroporto_de_destino_nome'])['passageiros_total'].sum().reset_index()
trajeto_mais_procurado = trajeto_mais_procurado.sort_values(by=['trimestre', 'passageiros_total'], ascending=[True, False])
trajeto_mais_procurado = trajeto_mais_procurado.groupby('trimestre').first().reset_index()

st.write("""Esta tabela mostra os trajetos mais procurados em cada trimestre""")
st.dataframe(trajeto_mais_procurado)
fig = px.bar(
    trajeto_mais_procurado, 
    x='trimestre', y='passageiros_total', 
    text='passageiros_total', 
    labels={'trimestre': 'Trimestre', 'passageiros_total': 'Passageiros Total'}, 
    title='Valores dos trajetos mais procurados por cada trimestre'
)
st.plotly_chart(fig)

st.write("")
st.write("")
st.write("""
    ### Análise temporal mensal
    Esta análise mostrará qual mês de cada ano teve a maior procura com o maior número de viagens do ano
""")
# Supondo que o DataFrame se chama df
# Criar uma coluna com o total de passageiros
df_sazonal_sem_groupby['passageiros_total'] = df_sazonal_sem_groupby['passageiros_pagos'] + df_sazonal_sem_groupby['passageiros_gratis']

# Agrupar por ano e mês e calcular a soma dos passageiros
grupo_ano_mes = df_sazonal_sem_groupby.groupby(['ano', 'mes'])['passageiros_total'].sum().reset_index()

# Encontrar o mês com maior procura para cada ano
mes_mais_procurado = grupo_ano_mes.loc[grupo_ano_mes.groupby('ano')['passageiros_total'].idxmax()]
st.dataframe(mes_mais_procurado)

fig = px.bar(
    mes_mais_procurado, 
    x='ano', y='mes', 
    text='passageiros_total', 
    labels={'mes': 'Mês', 'ano': 'Ano'}, 
    title='Mês com Maior Procura por Ano'
)
st.plotly_chart(fig)

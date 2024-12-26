import streamlit as st

from app import df_rotas, df_tam


st.write("""
# Análise Temporal
## Padrões Sazonais
Identificação de variações sazonais na demanda de passageiros e ajuste da oferta de voos de acordo.
""")


st.write("""
## Histórico de Voos
Comparação de dados históricos para detectar tendências e prever futuras demandas.
""")
import streamlit as st

from principal import df_rotas, df_tam


st.write("""
# Eficiência Operacional
## Taxa de Ocupação
Porcentagem de assentos ocupados em cada voo, ajudando a identificar voos com baixa demanda.
""")


st.write("""
## Decolagens e Pousos
Monitoramento do número de decolagens e pousos para otimização do uso das aeronaves.
""")
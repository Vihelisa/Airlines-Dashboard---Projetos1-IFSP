import streamlit as st
import matplotlib.pyplot as plt
from principal import df_rotas, df_tam


st.write("""
# Análise de Rota
## Desempenho de Rotas
Comparação entre diferentes rotas para identificar as mais e menos lucrativas. Para calcular a lucratividade é preciso dividir o RPK pela ASK e pegar como base 1 para saber se é alta ou baixa, ou seja, a cima de 1 é alta se não é baixa.
""")
df_tam.loc[:, 'coef_lucratividade'] = df_tam['rpk']/df_tam['ask']
df_lucratividade = df_tam[['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano', 'coef_lucratividade']]
df_lucratividade = df_lucratividade.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
df_lucratividade.loc[:, 'lucratividade'] = df_lucratividade['coef_lucratividade'].apply(lambda x: 'Alta' if x >= 1 else 'Baixa')
st.dataframe(df_lucratividade)


# Selecionar ano 
lista_ano = ['Todos']
anos = df_lucratividade['ano'].to_list()
ano_list = lista_ano + anos
ano_selecionado = st.selectbox('Selecione o Ano', ano_list) # Filtrar dados pelo ano selecionado df_ano = df[df['Ano'] == ano_selecionado]

df_ano = df_lucratividade[df_lucratividade['ano'] == ano_selecionado]

# Plotar gráficos 
fig, ax = plt.subplots(2, 1, figsize=(10, 8)) 
# Gráfico da rota mais lucrativa 
rota_mais_lucrativa_ano = df_ano.loc[df_ano['Lucratividade'].idxmax()] 
ax[0].plot(df_ano['Mês'], rota_mais_lucrativa_ano['Lucratividade']) 
ax[0].set_title('Rota Mais Lucrativa no Ano Selecionado') 
ax[0].set_xlabel('Mês') 
ax[0].set_ylabel('Lucratividade') 

# Gráfico da rota menos lucrativa 
rota_menos_lucrativa_ano = df_ano.loc[df_ano['Lucratividade'].idxmin()] 
ax[1].plot(df_ano['Mês'], rota_menos_lucrativa_ano['Lucratividade']) 
ax[1].set_title('Rota Menos Lucrativa no Ano Selecionado') 
ax[1].set_xlabel('Mês') 
ax[1].set_ylabel('Lucratividade') 
st.pyplot(fig)

st.write("""
## Distância Voada
Avaliação da distância média voada por rota e análise de possíveis otimizações.
""")
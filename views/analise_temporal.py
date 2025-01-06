import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
import matplotlib.pyplot as plt

from principal import df_rotas, df_tam


st.write("""
# Análise Temporal
## Padrões Sazonais
Identificação de variações sazonais na demanda de passageiros e ajuste da oferta de voos de acordo.
""")


st.write("""
## Histórico de Voos
Comparação de dados históricos para detectar tendências e prever futuras demandas.
""")
X = df_tam[['ano', 'mes']]
y_pagos = df_tam['passageiros_pagos']
y_gratis = df_tam['passageiros_gratis']

# Dividir os dados em treino e teste 
X_train, X_test, y_train_pagos, y_test_pagos = train_test_split(X, y_pagos, test_size=0.2, random_state=42) 
X_train, X_test, y_train_gratis, y_test_gratis = train_test_split(X, y_gratis, test_size=0.2, random_state=42)

# Criar e treinar o modelo para passageiros pagos 
modelo_pagos = LinearRegression() 
modelo_pagos.fit(X_train, y_train_pagos)

# Criar e treinar o modelo para passageiros grátis 
modelo_gratis = LinearRegression() 
modelo_gratis.fit(X_train, y_train_gratis)

# Fazer previsões 
y_pred_pagos = modelo_pagos.predict(X_test) 
y_pred_gratis = modelo_gratis.predict(X_test)

# Configuração do Streamlit 
st.title("Análise e Previsão de Demanda de Voos (Pagos e Grátis)") 
# Exibir dados
st.write("Dados de Voos:") 
st.dataframe(df_tam)

# Exibir coeficientes do modelo para passageiros pagos 
st.write("Coeficientes do Modelo para Passageiros Pagos:") 
st.write(f"Coeficientes: {modelo_pagos.coef_}") 
st.write(f"Intercepto: {modelo_pagos.intercept_}")

# Exibir coeficientes do modelo para passageiros grátis 
st.write("Coeficientes do Modelo para Passageiros Grátis:") 
st.write(f"Coeficientes: {modelo_gratis.coef_}") 
st.write(f"Intercepto: {modelo_gratis.intercept_}")

st.write("""
###### O gráfico mostra a relação entre os valores reais de passageiros (no eixo x) e as previsões feitas pelo modelo (no eixo y). Os pontos azuis representam os dados reais versus as previsões, e a linha preta tracejada representa a linha de identidade, onde as previsões seriam exatamente iguais aos valores reais.
###### A proximidade dos pontos azuis à linha preta tracejada indica a precisão das previsões. Pontos próximos à linha preta indicam previsões precisas, enquanto pontos acima ou abaixo da linha indicam superestimações ou subestimações, respectivamente.
""")

# Plotar previsões vs valores reais para passageiros pagos 
st.write("### Previsões vs Valores Reais para Passageiros Pagos:") 
fig1, ax1 = plt.subplots(figsize=(8, 4)) 
# Ajuste o tamanho da figura conforme necessário 
ax1.scatter(y_test_pagos, y_pred_pagos) 
ax1.plot([y_pagos.min(), y_pagos.max()], [y_pagos.min(), y_pagos.max()], 'k--', lw=4) 
ax1.set_xlabel('Valores Reais') 
ax1.set_ylabel('Previsões') 
st.pyplot(fig1) 


# Plotar previsões vs valores reais para passageiros grátis 
st.write("### Previsões vs Valores Reais para Passageiros Grátis:") 
fig2, ax2 = plt.subplots(figsize=(8, 4)) 
# Ajuste o tamanho da figura conforme necessário 
ax2.scatter(y_test_gratis, y_pred_gratis) 
ax2.plot([y_gratis.min(), y_gratis.max()], [y_gratis.min(), y_gratis.max()], 'k--', lw=4) 
ax2.set_xlabel('Valores Reais') 
ax2.set_ylabel('Previsões') 
st.pyplot(fig2)
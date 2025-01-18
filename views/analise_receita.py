import streamlit as st
import plotly.graph_objs as go
from principal import df_rotas, df_tam

# Função para colorir as células 
def colorir_celulas(val): 
    color = 'green' if val == 'Alta' else 'red' 
    return f'background-color: {color}'

def colorir_celulas2(val): 
    color = 'green' if val == 'Bom' else 'red' 
    return f'background-color: {color}'


st.write("""
# Análise de Rota
## Desempenho de Rotas
Comparação entre diferentes rotas para identificar as mais e menos lucrativas. 
###### Para calcular a lucratividade é preciso dividir o RPK pela ASK e pegar como base 1 para saber se é alta ou baixa, ou seja, a cima de 1 é alta se não é baixa.
""")
df_tam.loc[:, 'coef_lucratividade'] = df_tam['rpk']/df_tam['ask']
df_lucratividade = df_tam[['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano', 'coef_lucratividade']]
df_lucratividade = df_lucratividade.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
df_lucratividade.loc[:, 'lucratividade'] = df_lucratividade['coef_lucratividade'].apply(lambda x: 'Alta' if x >= 1 else 'Baixa')
df_lucratividade = df_lucratividade.drop(columns=['mes'])
df_styled = df_lucratividade.style.applymap(colorir_celulas, subset=['lucratividade'])
#st.dataframe(df_styled.data)
# Exibir o DataFrame estilizado com rolagem no Streamlit 
st.dataframe(df_styled, use_container_width=True)


# Selecionar ano 
lista_ano = ['Todos']
df_traf_ano = df_lucratividade.groupby(['ano']).sum().reset_index()
anos = df_traf_ano['ano'].astype(str).to_list()
ano_list = lista_ano + anos

st.write("")
st.write("")
ano_selecionado = st.selectbox('Selecione o Ano', ano_list) # Filtrar dados pelo ano selecionado df_ano = df[df['Ano'] == ano_selecionado]

if 'Todos' in ano_selecionado:
    df_lucrat_filter = df_lucratividade.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'lucratividade']).sum().reset_index()
    df_lucrat_filter = df_lucrat_filter.drop(columns=['ano'])
    # Encontrar as linhas com o valor mais alto e mais baixo na coluna 'total_passageiros'
    linha_valor_mais_alto = df_lucrat_filter.loc[df_lucrat_filter['coef_lucratividade'].idxmax()] 
    linha_valor_mais_baixo = df_lucrat_filter.loc[df_lucrat_filter['coef_lucratividade'].idxmin()]
        
    #Tratamento do df do valor mais alto:
    df_maior = df_lucratividade.loc[(df_lucratividade['aeroporto_de_origem_nome'] == linha_valor_mais_alto['aeroporto_de_origem_nome']) & (df_lucratividade['aeroporto_de_destino_nome'] == linha_valor_mais_alto['aeroporto_de_destino_nome'])]
    df_filtro_maior = df_maior.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
    df_filtro_maior['coef_lucratividade'] = df_filtro_maior['coef_lucratividade'].round(2)

    #Tratamento do df do valor mais baixo:
    df_menor = df_lucratividade.loc[(df_lucratividade['aeroporto_de_origem_nome'] == linha_valor_mais_baixo['aeroporto_de_origem_nome']) & (df_lucratividade['aeroporto_de_destino_nome'] == linha_valor_mais_baixo['aeroporto_de_destino_nome'])]
    df_filtro_menor = df_menor.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
    df_filtro_menor['coef_lucratividade'] = df_filtro_menor['coef_lucratividade'].round(2)


    # Definir as colunas 
    col1, col2 = st.columns(2)

    # Adicionar os widgets multiselect em colunas separadas 
    with col1: 
        st.write("")
        st.write("")
        st.write("Dados do trajeto com a maior lucratividade pela alta procura dos passajeitos")
        st.dataframe(linha_valor_mais_alto)
        st.dataframe(df_filtro_maior)
    with col2: 
        st.write("")
        st.write("")
        st.write("Dados do trajeto com a menor lucratividade devida a baixa procura dos passajeitos")
        st.dataframe(linha_valor_mais_baixo)
        st.dataframe(df_filtro_menor)

    trajeto_maior = df_filtro_maior['aeroporto_de_origem_nome'] + '-' + df_filtro_maior['aeroporto_de_destino_nome']
    trajeto_menor = df_filtro_menor['aeroporto_de_origem_nome']+ '-' + df_filtro_menor['aeroporto_de_destino_nome']
    
    fig = go.Figure() 
    # Adicionar barras para total_passageiros 
    fig.add_trace(go.Bar(x=df_filtro_maior['ano'], y=df_filtro_maior['coef_lucratividade'], 
                            name='Maior lucartividade', 
                            marker_color='green',
                            text=df_filtro_maior['coef_lucratividade'],
                            textposition='auto')) 
    # Adicionar barras para passageiros_pagos 
    fig.add_trace(go.Bar(x=df_filtro_menor['ano'], y=df_filtro_menor['coef_lucratividade'], 
                            name='Menor lucratividade',
                            marker_color='red',
                            text=df_filtro_menor['coef_lucratividade'],
                            textposition='auto')) 

    # Ajustar layout 
    fig.update_layout( 
        title='Gráfico da comparação entre o trecho de maior e menor lucratividade', 
        xaxis=dict(title='Ano'), 
        yaxis=dict(title='Lucratividade'), 
        barmode='group' # Agrupar barras lado a lado 
    )
    # Exibir o gráfico no Streamlit 
    st.plotly_chart(fig)

elif len(ano_selecionado) > 0:
    select_ano = [int(ano_selecionado)]
    df_lucratividade_groupby_mes = df_tam[['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano', 'coef_lucratividade']]
    df_lucratividade_mes = df_lucratividade_groupby_mes.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
    df_lucratividade_mes.loc[:, 'lucratividade'] = df_lucratividade_mes['coef_lucratividade'].apply(lambda x: 'Alta' if x >= 1 else 'Baixa')

    df_lucrat_filter = df_lucratividade_mes[df_lucratividade_mes['ano'].isin(select_ano)]

    
    # Encontrar as linhas com o valor mais alto e mais baixo na coluna 'total_passageiros'
    linha_valor_mais_alto = df_lucrat_filter.loc[df_lucrat_filter['coef_lucratividade'].idxmax()] 
    linha_valor_mais_baixo = df_lucrat_filter.loc[df_lucrat_filter['coef_lucratividade'].idxmin()]
        
    #Tratamento do df do valor mais alto:
    df_maior = df_lucrat_filter.loc[(df_lucrat_filter['aeroporto_de_origem_nome'] == linha_valor_mais_alto['aeroporto_de_origem_nome']) & (df_lucrat_filter['aeroporto_de_destino_nome'] == linha_valor_mais_alto['aeroporto_de_destino_nome'])]
    df_filtro_maior = df_maior.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
    df_filtro_maior['coef_lucratividade'] = df_filtro_maior['coef_lucratividade'].round(2)

    #Tratamento do df do valor mais baixo:
    df_menor = df_lucrat_filter.loc[(df_lucrat_filter['aeroporto_de_origem_nome'] == linha_valor_mais_baixo['aeroporto_de_origem_nome']) & (df_lucrat_filter['aeroporto_de_destino_nome'] == linha_valor_mais_baixo['aeroporto_de_destino_nome'])]
    df_filtro_menor = df_menor.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
    df_filtro_menor['coef_lucratividade'] = df_filtro_menor['coef_lucratividade'].round(2)

    # Definir as colunas 
    col1, col2 = st.columns(2)

    # Adicionar os widgets multiselect em colunas separadas 
    with col1: 
        st.write("")
        st.write("")
        st.write("Dados do trajeto com a maior lucratividade pela alta procura dos passajeitos")
        st.dataframe(linha_valor_mais_alto)
        st.dataframe(df_filtro_maior)
    with col2: 
        st.write("")
        st.write("")
        st.write("Dados do trajeto com a menor lucratividade devida a baixa procura dos passajeitos")
        st.dataframe(linha_valor_mais_baixo)
        st.dataframe(df_filtro_menor)

    trajeto_maior = df_filtro_maior['aeroporto_de_origem_nome'] + '-' + df_filtro_maior['aeroporto_de_destino_nome']
    trajeto_menor = df_filtro_menor['aeroporto_de_origem_nome']+ '-' + df_filtro_menor['aeroporto_de_destino_nome']
    
    fig = go.Figure() 
    # Adicionar barras para total_passageiros 
    fig.add_trace(go.Bar(x=df_filtro_maior['mes'], y=df_filtro_maior['coef_lucratividade'], 
                            name='Maior lucartividade', 
                            marker_color='green',
                            text=df_filtro_maior['coef_lucratividade'],
                            textposition='auto')) 
    # Adicionar barras para passageiros_pagos 
    fig.add_trace(go.Bar(x=df_filtro_menor['mes'], y=df_filtro_menor['coef_lucratividade'], 
                            name='Menor lucratividade',
                            marker_color='red',
                            text=df_filtro_menor['coef_lucratividade'],
                            textposition='auto')) 

    # Ajustar layout 
    fig.update_layout( 
        title='Gráfico da comparação entre o trecho de maior e menor lucratividade', 
        xaxis=dict(title='Mês'), 
        yaxis=dict(title='Lucratividade'), 
        barmode='group' # Agrupar barras lado a lado 
    )
    # Exibir o gráfico no Streamlit 
    st.plotly_chart(fig)


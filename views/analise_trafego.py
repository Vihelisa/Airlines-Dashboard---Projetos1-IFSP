import streamlit as st
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid
import plotly.graph_objs as go

from principal import df_tam
from functions.functions import *


st.write("""
# Análise de Tráfego Aereo
## Volume de Passageiros
Análise do número total de passageiros por rota e período de mês e ano.
""")
#filtrando dataframe para usar na tela
df_trafego = df_tam[['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano', 'passageiros_pagos', 'passageiros_gratis']]
df_trafego.loc[:, 'total_passageiros'] = df_trafego['passageiros_pagos'] + df_trafego['passageiros_gratis']
df_trafego['total_passageiros'] = df_trafego['total_passageiros'].astype(int)

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
"""lista_ano = list(df_traf_ano['ano'].unique()) 
lista_ano.insert(0, 'Todos')"""


# Definir as colunas 
col1, col2, col3 = st.columns(3)

# Adicionar os widgets multiselect em colunas separadas 
with col1: 
    select_trageto = st.multiselect("Selecione o trajeto", lista_trageto)
with col2: 
    select_ano = st.multiselect("Selecione o ano", lista_ano)
with col3:
    info_num = st.number_input('Insira um número inteiro como parâmetro de comparação: ', step=1)

select_trafego, select_ano = filter_empty_data(select_trageto, select_ano)

# Função para colorir as células 
def colorir_celulas(val): 
    color = 'green' if val == 'Bom' else 'red' 
    return f'background-color: {color}'

if 'Todos' in select_trageto:
    if 'Todos' in select_ano:
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes', 'ano'])
        df_traf_all_filtered['parametro'] = info_num
        df_traf_all_filtered['analise_de_frequencia'] = df_traf_all_filtered.apply(lambda row: 'Bom' if row['total_passageiros'] >= row['parametro'] else 'Baixo', axis=1)
        df_styled = df_traf_all_filtered.style.applymap(colorir_celulas, subset=['analise_de_frequencia'])
        #st.dataframe(df_styled.data)
        # Exibir o DataFrame estilizado com rolagem no Streamlit 
        st.write(f""" 
                <div style="height:500px;overflow-y:scroll;"> 
                    {df_styled.to_html(escape=False)} 
                """, unsafe_allow_html=True
        )

        # Encontrar as linhas com o valor mais alto e mais baixo na coluna 'total_passageiros'
        linha_valor_mais_alto = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmax()] 
        linha_valor_mais_baixo = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmin()]
        
        #Tratamento do df do valor mais alto:
        df_maior = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_alto['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_alto['aeroporto_de_destino_nome'])]
        df_filtro_maior = df_maior.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_filtro_maior = df_filtro_maior.drop(columns=['mes'])

        #Tratamento do df do valor mais baixo:
        df_menor = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_baixo['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_baixo['aeroporto_de_destino_nome'])]
        df_filtro_menor = df_menor.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_filtro_menor = df_filtro_menor.drop(columns=['mes'])
        
        st.write("")
        st.write("")
        st.write("""
        Estes sãos os trajetos com a maior e a menos frequencia de passageiros relacionados a todos os anos analisados. Considere que o maior valor foi o trajeto mais procurado e o menor o de menos interesse dos viajantes.
        """)


        st.write("""#### VALOR MAIS ALTO:""")
        st.dataframe(linha_valor_mais_alto)
        st.dataframe(df_filtro_maior)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig.add_trace(go.Bar(x=df_filtro_maior['ano'], y=df_filtro_maior['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_maior['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig.add_trace(go.Bar(x=df_filtro_maior['ano'], y=df_filtro_maior['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_maior['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig.add_trace(go.Bar(x=df_filtro_maior['ano'], y=df_filtro_maior['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_maior['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig)

        st.write("")
        st.write("""#### VALOR MAIS BAIXO:""")
        st.dataframe(linha_valor_mais_baixo)
        st.dataframe(df_filtro_menor)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig.add_trace(go.Bar(x=df_filtro_menor['ano'], y=df_filtro_menor['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_menor['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig.add_trace(go.Bar(x=df_filtro_menor['ano'], y=df_filtro_menor['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_menor['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig.add_trace(go.Bar(x=df_filtro_menor['ano'], y=df_filtro_menor['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_menor['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig)

    else:
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes'])
        df_traf_all_filtered = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        df_traf_all_filtered['parametro'] = info_num
        df_traf_all_filtered['analise_de_frequencia'] = df_traf_all_filtered.apply(lambda row: 'Bom' if row['total_passageiros'] >= row['parametro'] else 'Baixo', axis=1)
        df_styled = df_traf_all_filtered.style.applymap(colorir_celulas, subset=['analise_de_frequencia'])
        # Exibir o DataFrame estilizado com rolagem no Streamlit 
        st.write(f""" 
                <div style="height:500px;overflow-y:scroll;"> 
                    {df_styled.to_html(escape=False)} 
                """, unsafe_allow_html=True
        )

        # Encontrar as linhas com o valor mais alto e mais baixo na coluna 'total_passageiros'
        linha_valor_mais_alto = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmax()] 
        linha_valor_mais_baixo = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmin()]

        #Tratamento do df do valor mais alto:
        df_maior = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_alto['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_alto['aeroporto_de_destino_nome'])]
        df_filtro_maior = df_maior.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_filtro_maior = df_filtro_maior[df_filtro_maior['ano'].isin(select_ano)]

        #Tratamento do df do valor mais baixo:
        df_menor = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_baixo['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_baixo['aeroporto_de_destino_nome'])]
        df_filtro_menor = df_menor.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_filtro_menor = df_filtro_menor[df_filtro_menor['ano'].isin(select_ano)]

        st.write("")
        st.write("")
        st.write("""
        Estes sãos os trajetos com a maior e a menos frequencia de passageiros relacionados a todos os anos analisados. Considere que o maior valor foi o trajeto mais procurado e o menor o de menos interesse dos viajantes.
        """)


        st.write("""#### VALOR MAIS ALTO:""")
        st.dataframe(linha_valor_mais_alto)
        st.dataframe(df_filtro_maior)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig.add_trace(go.Bar(x=df_filtro_maior['mes'], y=df_filtro_maior['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_maior['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig.add_trace(go.Bar(x=df_filtro_maior['mes'], y=df_filtro_maior['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_maior['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig.add_trace(go.Bar(x=df_filtro_maior['mes'], y=df_filtro_maior['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_maior['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig)

        st.write("")
        st.write("""#### VALOR MAIS BAIXO:""")
        st.dataframe(linha_valor_mais_baixo)
        st.dataframe(df_filtro_menor)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig.add_trace(go.Bar(x=df_filtro_menor['mes'], y=df_filtro_menor['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_menor['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig.add_trace(go.Bar(x=df_filtro_menor['mes'], y=df_filtro_menor['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_menor['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig.add_trace(go.Bar(x=df_filtro_menor['mes'], y=df_filtro_menor['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_menor['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig)

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
        df_traf_all_filtered['parametro'] = info_num
        df_traf_all_filtered['analise_de_frequencia'] = df_traf_all_filtered.apply(lambda row: 'Bom' if row['total_passageiros'] >= row['parametro'] else 'Baixo', axis=1)
        df_styled = df_traf_all_filtered.style.applymap(colorir_celulas, subset=['analise_de_frequencia'])
        # Exibir o DataFrame estilizado com rolagem no Streamlit 
        st.write(f""" 
                <div style="height:500px;overflow-y:scroll;"> 
                    {df_styled.to_html(escape=False)} 
                """, unsafe_allow_html=True
        )
        # Encontrar as linhas com o valor mais alto e mais baixo na coluna 'total_passageiros'
        linha_valor_mais_alto = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmax()] 
        linha_valor_mais_baixo = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmin()]
        
        #Tratamento do df do valor mais alto:
        df_maior = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_alto['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_alto['aeroporto_de_destino_nome'])]
        df_filtro_maior = df_maior.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_filtro_maior = df_filtro_maior.drop(columns=['mes'])

        #Tratamento do df do valor mais baixo:
        df_menor = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_baixo['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_baixo['aeroporto_de_destino_nome'])]
        df_filtro_menor = df_menor.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_filtro_menor = df_filtro_menor.drop(columns=['mes'])
        
        st.write("")
        st.write("")
        st.write("""
        Estes sãos os trajetos com a maior e a menos frequencia de passageiros relacionados a todos os anos analisados. Considere que o maior valor foi o trajeto mais procurado e o menor o de menos interesse dos viajantes.
        """)


        st.write("""#### VALOR MAIS ALTO:""")
        st.dataframe(linha_valor_mais_alto)
        st.dataframe(df_filtro_maior)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig1 = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig1.add_trace(go.Bar(x=df_filtro_maior['ano'], y=df_filtro_maior['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_maior['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig1.add_trace(go.Bar(x=df_filtro_maior['ano'], y=df_filtro_maior['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_maior['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig1.add_trace(go.Bar(x=df_filtro_maior['ano'], y=df_filtro_maior['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_maior['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig1.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig1, key='grafico1')

        st.write("")
        st.write("""#### VALOR MAIS BAIXO:""")
        st.dataframe(linha_valor_mais_baixo)
        st.dataframe(df_filtro_menor)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig2 = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig2.add_trace(go.Bar(x=df_filtro_menor['ano'], y=df_filtro_menor['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_menor['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig2.add_trace(go.Bar(x=df_filtro_menor['ano'], y=df_filtro_menor['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_menor['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig2.add_trace(go.Bar(x=df_filtro_menor['ano'], y=df_filtro_menor['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_menor['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig2.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig2, key='grafico2')

    else:
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_ordenado.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano', 'mes']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        df_traf_all_filtered['parametro'] = info_num
        df_traf_all_filtered['analise_de_frequencia'] = df_traf_all_filtered.apply(lambda row: 'Bom' if row['total_passageiros'] >= row['parametro'] else 'Baixo', axis=1)
        df_styled = df_traf_all_filtered.style.applymap(colorir_celulas, subset=['analise_de_frequencia'])
        # Exibir o DataFrame estilizado com rolagem no Streamlit 
        st.write(f""" 
                <div style="height:500px;overflow-y:scroll;"> 
                    {df_styled.to_html(escape=False)} 
                """, unsafe_allow_html=True
        )
    
        # Encontrar as linhas com o valor mais alto e mais baixo na coluna 'total_passageiros'
        linha_valor_mais_alto = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmax()] 
        linha_valor_mais_baixo = df_traf_all_filtered.loc[df_traf_all_filtered['total_passageiros'].idxmin()]

        #Tratamento do df do valor mais alto:
        df_maior = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_alto['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_alto['aeroporto_de_destino_nome'])]
        df_filtro_maior = df_maior.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_filtro_maior = df_filtro_maior[df_filtro_maior['ano'].isin(select_ano)]

        #Tratamento do df do valor mais baixo:
        df_menor = df_trafego.loc[(df_trafego['aeroporto_de_origem_nome'] == linha_valor_mais_baixo['aeroporto_de_origem_nome']) & (df_trafego['aeroporto_de_destino_nome'] == linha_valor_mais_baixo['aeroporto_de_destino_nome'])]
        df_filtro_menor = df_menor.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_filtro_menor = df_filtro_menor[df_filtro_menor['ano'].isin(select_ano)]

        st.write("")
        st.write("")
        st.write("""
        Estes sãos os trajetos com a maior e a menos frequencia de passageiros relacionados a todos os anos analisados. Considere que o maior valor foi o trajeto mais procurado e o menor o de menos interesse dos viajantes.
        """)


        st.write("""#### VALOR MAIS ALTO:""")
        st.dataframe(linha_valor_mais_alto)
        st.dataframe(df_filtro_maior)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig.add_trace(go.Bar(x=df_filtro_maior['mes'], y=df_filtro_maior['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_maior['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig.add_trace(go.Bar(x=df_filtro_maior['mes'], y=df_filtro_maior['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_maior['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig.add_trace(go.Bar(x=df_filtro_maior['mes'], y=df_filtro_maior['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_maior['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig, key='grafico1')

        st.write("")
        st.write("""#### VALOR MAIS BAIXO:""")
        st.dataframe(linha_valor_mais_baixo)
        st.dataframe(df_filtro_menor)

        #####GRÁFICO 
        # Criar o gráfico de barras 
        fig = go.Figure() 
        # Adicionar barras para total_passageiros 
        fig.add_trace(go.Bar(x=df_filtro_menor['mes'], y=df_filtro_menor['total_passageiros'], 
                             name='Total Passageiros', 
                             marker_color='blue',
                             text=df_filtro_menor['total_passageiros'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_pagos 
        fig.add_trace(go.Bar(x=df_filtro_menor['mes'], y=df_filtro_menor['passageiros_pagos'], 
                             name='Passageiros Pagos', 
                             marker_color='green',
                             text=df_filtro_menor['passageiros_pagos'],
                             textposition='auto')) 
        # Adicionar barras para passageiros_gratis 
        fig.add_trace(go.Bar(x=df_filtro_menor['mes'], y=df_filtro_menor['passageiros_gratis'], 
                             name='Passageiros Grátis', 
                             marker_color='red',
                             text=df_filtro_menor['passageiros_gratis'],
                             textposition='auto'))
        # Ajustar layout 
        fig.update_layout( 
            title='Gráfico de Total Passageiros, Passageiros Pagos e Passageiros Grátis por Ano para o trageto com a maior análise', 
            xaxis=dict(title='Ano'), 
            yaxis=dict(title='Quantidade de Passageiros'), 
            barmode='group' # Agrupar barras lado a lado 
        )
        # Exibir o gráfico no Streamlit 
        st.plotly_chart(fig, key='grafico2')

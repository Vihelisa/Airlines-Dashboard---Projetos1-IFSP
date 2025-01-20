import streamlit as st
import plotly.graph_objs as go
#from principal import df_emp_filtro
from config.consulta import get_query


# Função para colorir as células 
def colorir_celulas(val): 
    color = 'green' if val == 'Alto' else 'red' 
    return f'background-color: {color}'

def colorir_celulas2(val): 
    color = 'green' if val == 'Bom' else 'red' 
    return f'background-color: {color}'


df_funcionario, df_empresa, df_rotas = get_query()
df_id_empresa = df_funcionario.loc[df_funcionario['email'] == st.session_state.user_email, 'id_empresa'].reset_index()
id_empresa = df_id_empresa['id_empresa'][0]
df_emp_filtro = df_rotas.loc[df_rotas['id_empresa']==id_empresa]


st.write("""
## Distância Voada
Avaliação da distância média voada por rota e análise de possíveis otimizações.
""")

df_distancia = df_emp_filtro[['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano', 'distancia_voada_km', 'decolagens', 'horas_voadas']]
df_distancia_groupby = df_distancia.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).agg({
    'distancia_voada_km': 'mean',
    'decolagens': 'mean',
    'horas_voadas': 'mean'
}).reset_index()

lista_aerop_origem = df_distancia_groupby['aeroporto_de_origem_nome'].to_list()
lista_aerop_destino = df_distancia_groupby['aeroporto_de_destino_nome'].to_list()
lista_trageto = []
for num in range(len(lista_aerop_origem)):
    trageto = f'{lista_aerop_origem[num]} - {lista_aerop_destino[num]}'
    lista_trageto.append(trageto)

lista_trajeto_tratada = list(set(lista_trageto))

df_distancia_groupby.rename(columns={ 
    'aeroporto_de_origem_nome': 'Aeroporto de Origem',
    'aeroporto_de_destino_nome': 'Aeroporto de Destino',
    'distancia_voada_km': 'Média anual de distância voada (KM)', 
    'numero_decolagens': 'Média de decolagens anual', 
    'horas_voadas': 'Média de horas voadas anual' }, inplace=True)


select_trageto = st.selectbox("Selecione o trajeto", lista_trajeto_tratada)   


if len(select_trageto) > 0:
    nomes_separados = select_trageto.split(' - ')
    df_filtrado = df_distancia_groupby.loc[(df_distancia_groupby['Aeroporto de Origem'] == nomes_separados[0]) & (df_distancia_groupby['Aeroporto de Destino'] == nomes_separados[1])]
    df_filtrado['Média Total'] = df_filtrado['Média anual de distância voada (KM)'].mean().round(2)
    df_filtrado['Análise'] = df_filtrado.apply(lambda row: 'Alto' if row['Média anual de distância voada (KM)'] >= row['Média Total'] else 'Baixo', axis=1)
    df_filtrado = df_filtrado.round(2)
    df_styled = df_filtrado.style.applymap(colorir_celulas, subset=['Análise'])
    st.dataframe(df_styled, use_container_width=True)



    fig = go.Figure() 
    # Adicionar barras para total_passageiros 
    fig.add_trace(go.Bar(x=df_filtrado['ano'], y=df_filtrado['Média anual de distância voada (KM)'], 
                            name='Média anual de distância voada (KM)', 
                            marker_color='blue',
                            text=df_filtrado['Média anual de distância voada (KM)'],
                            textposition='auto')) 
    # Adicionar barras para passageiros_pagos 
    fig.add_trace(go.Bar(x=df_filtrado['ano'], y=df_filtrado['decolagens'], 
                            name='Média de decolagens anual', 
                            marker_color='green',
                            text=df_filtrado['decolagens'],
                            textposition='auto')) 
    # Adicionar barras para passageiros_gratis 
    fig.add_trace(go.Bar(x=df_filtrado['ano'], y=df_filtrado['Média de horas voadas anual'], 
                            name='Média de horas voadas anual', 
                            marker_color='red',
                            text=df_filtrado['Média de horas voadas anual'],
                            textposition='auto'))
    # Ajustar layout 
    fig.update_layout( 
        title='Gráfico dos dados relacionados as distâncias voadas por cada trageto', 
        xaxis=dict(title='Ano'), 
        yaxis=dict(title='Valores relacionados a distância'), 
        barmode='group' # Agrupar barras lado a lado 
    )
    # Exibir o gráfico no Streamlit 
    st.plotly_chart(fig)

    """
    ### Análise de tendência
    Nesta análise de tendência é visto se ao longo dos anos houve um aumento ou diminuição na distância, horas voadas e quantidade de decolagens. Se os valores forem negativos quer dizer que houve diminuição na categoria e se forem positivos houve aumento.
    """

    # Identificar possíveis otimizações
    def identificar_otimizacoes(df_filtrado):
        df_filtrado['Tendencia das decolagens'] = df_filtrado['decolagens'].diff()
        df_filtrado['Tendencia nas horas voadas'] = df_filtrado['Média de horas voadas anual'].diff()
        df_filtrado['Tendencia na distância voada'] = df_filtrado['Média anual de distância voada (KM)'].diff()
        return df_filtrado

    # Aplicar a função de otimizações para cada rota
    df_filtrado['Tendencia das decolagens'] = df_filtrado['decolagens'].diff()
    df_filtrado['Tendencia nas horas voadas'] = df_filtrado['Média de horas voadas anual'].diff()
    df_filtrado['Tendencia na distância voada'] = df_filtrado['Média anual de distância voada (KM)'].diff()
    tendencias_otimizadas = df_filtrado.drop(columns=['decolagens', 'Média de horas voadas anual', 'Média anual de distância voada (KM)', 'Análise'])
    #tendencias_otimizadas = tendencias_otimizadas.reset_index()
    st.dataframe(tendencias_otimizadas)
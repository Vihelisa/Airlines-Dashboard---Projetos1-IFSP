import secrets
import string
import streamlit as st
import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart



def load_css(file_name):
    '''
    Função que faz as modificações feitas em css serem carregadas pelo streamlit
    '''
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def change_page(new_page): 
    '''
    Função para mudar de página 
    '''
    st.session_state.page = new_page


def generate_secure_password(length=12):
    '''
    Função que gera senhas automaticamente para novos usuáirios
    '''
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


# Função para enviar email 
def send_email(to_email, password): 
    from_email = "airlinesdashboard@gmail.com" 
    from_password = "gbjlrvqwntnnslnk" 
    msg = MIMEMultipart() 
    msg['From'] = from_email 
    msg['To'] = to_email 
    msg['Subject'] = 'Sua Nova Senha' 
    body = f'Sua nova senha é: {password}' 
    msg.attach(MIMEText(body, 'plain'))
    try: 
        server = smtplib.SMTP('smtp.gmail.com', 587) 
        server.starttls() 
        server.login(from_email, from_password) 
        text = msg.as_string() 
        server.sendmail(from_email, to_email, text)
        server.quit() 
        st.success(f"Solicitação de cadastro enviada com sucesso! Email enviado para {to_email}") 
    except Exception as e: 
        st.error(f"Erro ao enviar email: {e}")

    
def filter_empty_data(select_trafego, select_mes, select_ano):
    if not select_trafego:
        select_trafego = 'Todos'
    if not select_mes:
        select_mes = 'Todos'
    if not select_ano:
        select_ano = 'Todos'
    return select_trafego, select_mes, select_ano



def multiselect_mes_ano_option(df_trafego, select_mes, select_ano):
    if 'Todos' in select_mes and 'Todos' in select_ano:
        print('Todos tem todos selecionados')
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes', 'ano'])
        return df_traf_all_filtered
    
    elif 'Todos' in select_mes and not 'Todos' in select_ano:
        print('apenas o ano é diferente')
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'ano']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['mes'])
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        return df_graph
    
    elif not 'Todos' in select_mes and 'Todos' in select_ano:
        print('Apenas o mes é diferente')
        select_mes = [int(item) for item in select_mes]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes']).sum().reset_index()
        df_traf_all_filtered = df_traf_todos.drop(columns=['ano'])
        df_graph = df_traf_all_filtered[df_traf_all_filtered['mes'].isin(select_mes)]
        return df_graph
    
    else:
        print('O mes e o ano são diferentes')
        select_mes = [int(item) for item in select_mes]
        select_ano = [int(item) for item in select_ano]
        df_traf_todos = df_trafego.groupby(['aeroporto_de_origem_nome', 'aeroporto_de_destino_nome', 'mes', 'ano']).sum().reset_index()
        df_graph = df_traf_todos[df_traf_todos['mes'].isin(select_mes)]
        df_graph = df_traf_todos[df_traf_todos['ano'].isin(select_ano)]
        return df_graph
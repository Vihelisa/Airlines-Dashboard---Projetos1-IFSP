import streamlit as st
from functions.functions import *


st.title("Perfil do usuário")  

try:
    if 'email' in st.session_state and 'senha' in st.session_state: 
        email = st.session_state.email 
        senha = st.session_state.senha 
    else:
        st.error("Usuário não logado. Faça login novamente.")
        st.session_state.page = 'login'
except:
    print('ainda não foi inserido')

# Busca as informações do usuário
user_info = fetch_user_info(email, senha)


# Layout
col1, col2 = st.columns(2)

with col1:
    # Ícone genérico de usuário
    st.image(
        "static/icons/iconeperfil.png",  # URL do ícone de usuário
        width=150,
        caption="Foto de Perfil",
    )


with col2:
    # Exibição das informações do usuário
    st.subheader("Informações Pessoais")
    st.write(f"**Nome:** {user_info['nome'][0]}")
    st.write(f"**Email:** {user_info['email'][0]}")
    st.write(f"**Cargo:** {user_info['cargo'][0]}")
    st.write(f"**Empresa:** {user_info['empresa_nome'][0]}")


# Botões de ação
if st.button("Alterar Senha"):
    st.session_state.page = 'alterar_senha'
if st.button("Sair"):
    st.session_state.logged_in = False
    st.session_state.page = 'login'
import streamlit as st
from functions.functions import *

def tela_perfil_user():
    st.title("Perfil do Usuário")

    # Verifica se o usuário está logado
    if 'user_id' not in st.session_state:
        st.error("Usuário não logado. Faça login novamente.")
        st.session_state.page = 'login'
        return

    # Busca as informações do usuário
    user_info = fetch_user_info(st.session_state.user_id)
    if not user_info:
        st.error("Não foi possível carregar as informações do perfil.")
        return

    # Layout
    col1, col2 = st.columns([1, 2])

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
        st.write(f"**Nome:** {user_info['nome']}")
        st.write(f"**Email:** {user_info['email']}")
        st.write(f"**Cargo:** {user_info['cargo']}")
        st.write(f"**Empresa:** {user_info['empresa']}")

    # Botões de ação
    st.button("Alterar Senha", on_click=lambda: change_page('alterar_senha'))
    

tela_perfil_user()
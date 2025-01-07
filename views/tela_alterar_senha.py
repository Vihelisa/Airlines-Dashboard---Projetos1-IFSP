import streamlit as st
from functions.functions import *

def tela_alterar_senha():
    """Tela dedicada para alteração de senha."""
    st.title("Alterar Senha")

    # Verifica se o usuário está logado
    if 'user_id' not in st.session_state:
        st.error("Usuário não logado. Faça login novamente.")
        st.session_state.page = 'login'
        return

    with st.form(key="form_alterar_senha"):
        senha_atual = st.text_input("Senha Atual", type="password")
        nova_senha = st.text_input("Nova Senha", type="password")
        confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
        
        alterar = st.form_submit_button("Alterar Senha")

        if alterar:
            # Lógica de validação e atualização
            if not senha_atual or not nova_senha or not confirmar_senha:
                st.warning("Por favor, preencha todos os campos.")
            elif not validate_user(st.session_state.user_email, senha_atual):
                st.error("Senha atual incorreta.")
            elif nova_senha != confirmar_senha:
                st.error("A nova senha e a confirmação não correspondem.")
            else:
                # Atualiza a senha no banco
                if atualizar_senha_bd(st.session_state.user_id, nova_senha):
                    st.success("Senha alterada com sucesso!")
                else:
                    st.error("Erro ao alterar a senha. Tente novamente.")

    if st.button("Voltar"):
        st.session_state.page = 'principal'  
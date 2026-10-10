import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cadastro de Pacientes", layout="centered")
st.title("Cadastro de Pacientes")

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]

# Cria a "memória" da sessão na primeira vez que o app abre
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

# Formulário: os campos só são enviados quando clicar no botão
with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
    )
    prioridade = st.slider("Prioridade do atendimento (5 = urgente)", 1, 5)
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar")

# O que acontece depois do clique
if enviado:
    if nome.strip() == "":
        st.warning("Por favor, preencha o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome,
            "idade": idade,
            "convenio": convenio,
            "prioridade": prioridade,
            "motivo": motivo,
        }
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha])],
            ignore_index=True,
        )
        st.success("Paciente cadastrado!")

# Tabela com os 5 últimos cadastros
st.subheader("Últimos pacientes cadastrados")
st.dataframe(st.session_state.pacientes.tail(5))

# Botão para baixar todos os cadastros da sessão em CSV
csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8-sig")
st.download_button("Baixar CSV", csv, "pacientes.csv", "text/csv")


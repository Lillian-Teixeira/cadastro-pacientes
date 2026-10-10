import gradio as gr
import pandas as pd
import os
from datetime import datetime

# Guarda o CSV na mesma pasta onde está este app.py
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "pacientes.csv")


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    # Não deixa cadastrar sem nome
    if not nome or nome.strip() == "":
        if os.path.exists(ARQUIVO_CSV):
            tabela_atual = pd.read_csv(ARQUIVO_CSV).tail(5)
        else:
            tabela_atual = None
        return "Por favor, preencha o nome do paciente.", tabela_atual

    # Monta a linha com os dados do formulário + data/hora
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": idade,
        "convenio": convenio,
        "prioridade": prioridade,
        "motivo": motivo,
    }
    novo = pd.DataFrame([linha])

    # Se o arquivo já existe, acrescenta; se não, cria com cabeçalho
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    return "Paciente cadastrado com sucesso!", pd.read_csv(ARQUIVO_CSV).tail(5)


with gr.Blocks() as demo:
    gr.Markdown("## Cadastro de Pacientes")

    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade", precision=0)
    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio",
        interactive=True,
    )
    prioridade = gr.Slider(1, 5, step=1, value=1, label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)

    botao = gr.Button("Cadastrar")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados")

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela],
    )

demo.launch()

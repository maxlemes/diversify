# Gerencia interatividade entre elementos do dashboard.
# Responde a eventos como cliques, seleções e atualizações.

from dash import Input, Output
from dashboard.app import app


@app.callback(Output('output-div', 'children'), Input('input-text', 'value'))
def atualizar_texto(valor):
    return f'Você digitou: {valor}'

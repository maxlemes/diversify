# Responsável por inicializar o Dash.
# Importa os layouts e callbacks.
# Define a estrutura base do aplicativo.
# Executa o servidor.

from dash import Dash
import dash_bootstrap_components as dbc
import dashboard.layouts  # Importa o layout
import dashboard.callbacks  # Garante que os callbacks sejam carregados

# Inicializa o app com Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define o layout do app
app.layout = dashboard.layouts.layout

# Executa o app
if __name__ == "__main__":
    app.run_server(debug=True)


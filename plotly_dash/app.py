import dash
import dash_bootstrap_components as dbc
from layouts import layout
import callbacks

# Inicializa o app com Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define o layout do app
app.layout = layout

# Executa o app
if __name__ == "__main__":
    app.run_server(debug=True)


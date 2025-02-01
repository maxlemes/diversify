import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

# Inicializando o app Dash com o tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Criando um exemplo de dataframe para o gráfico
df = pd.DataFrame({
    "Categoria": ["A", "B", "C", "D", "E"],
    "Valor": [10, 20, 30, 40, 50]
})

# Criando um gráfico de barras com Plotly
fig = px.bar(df, x="Categoria", y="Valor", title="Gráfico de Exemplo")

# Layout do Dashboard
app.layout = html.Div(
    [
        # Barra de navegação
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Sobre", href="/about")),
            ],
            brand="Dashboard Exemplo",
            brand_href="/",
            color="primary",
            dark=True,
        ),
        
        # Conteúdo principal do Dashboard
        dbc.Container(
            [
                # Título
                dbc.Row(
                    dbc.Col(html.H1("Dashboard Interativo", className="text-center"), width=12)
                ),
                
                # Gráfico
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=fig), width=12)
                ),
                
                # Card de Exemplo
                dbc.Row(
                    dbc.Col(dbc.Card(
                        dbc.CardBody([
                            html.H4("Card de Informações", className="card-title"),
                            html.P("Informações sobre o gráfico ou outros dados."),
                        ])
                    ), width=4)
                ),
                
                # Tabela de Exemplo
                dbc.Row(
                    dbc.Col(dbc.Table(
                        [
                            html.Thead(html.Tr([html.Th("Categoria"), html.Th("Valor")])),
                            html.Tbody([html.Tr([html.Td(c), html.Td(v)]) for c, v in zip(df["Categoria"], df["Valor"])])
                        ]
                    ), width=12)
                ),
            ],
            fluid=True  # Tornar o container fluido para ocupar toda a largura
        ),
    ]
)

# Rodar o app
if __name__ == "__main__":
    app.run_server(debug=True)


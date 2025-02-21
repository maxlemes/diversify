# Contém o layout do aplicativo (estrutura das páginas).
# Define os componentes visuais (gráficos, botões, texto etc.).
# Utiliza dbc.Row() e dbc.Col() para organização.

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.graficos import criar_grafico, grafico_comparativo

# Suponha que já temos os dados calculados
investimentos_total = 100000
aporte = 5000
patrimonio_total = investimentos_total + aporte
distribuicao_atual = {
    "Ações": 40000,
    "Renda Fixa": 30000,
    "FIIs": 20000,
    "Cripto": 10000,
}
distribuicao_desejada = {
    "Ações": 35000,
    "Renda Fixa": 35000,
    "FIIs": 20000,
    "Cripto": 15000,
}

layout = dbc.Container(
    [
        html.H1("Dashboard de Investimentos", className="text-center mb-4"),
        # Exibição de valores principais
        dbc.Row(
            [
                dbc.Col(
                    html.H3(
                        f"Valor Investido: R$ {investimentos_total:,.2f}",
                        className="text-primary text-center",
                    ),
                    width=6,
                ),
                dbc.Col(
                    html.H3(
                        f"Aporte: R$ {aporte:,.2f}",
                        className="text-success text-center",
                    ),
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        f"Patrimônio Total: R$ {patrimonio_total:,.2f}",
                        className="text-warning text-center",
                    ),
                    width=12,
                )
            ],
            className="mb-4",
        ),
        # Gráficos
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure=criar_grafico(
                            "rosca", distribuicao_atual, "Distribuição Atual"
                        )
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(
                        figure=criar_grafico(
                            "rosca",
                            distribuicao_desejada,
                            "Distribuição Desejada",
                        )
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        # Gráfico de barras comparando as distribuições
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure=grafico_comparativo(
                            distribuicao_atual, distribuicao_desejada
                        )
                    ),
                    width=12,
                ),
            ],
            className="mb-4",
        ),
    ]
)

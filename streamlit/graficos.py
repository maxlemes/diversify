# grafico.py
import plotly.graph_objects as go
import plotly.express as px

def criar_grafico(tipo, dados, titulo, cores, hole=0.4):
    """
    Função genérica para criar gráficos de rosca, barras ou treemap.
    
    :param tipo: Tipo do gráfico ('rosca', 'barras' ou 'treemap')
    :param dados: Dicionário com os dados a serem plotados
    :param titulo: Título do gráfico
    :param cores: Lista de cores para os gráficos
    :param hole: Para gráficos de rosca, define o tamanho do buraco central (default 0.4)
    :return: Gráfico Plotly configurado
    """
    if tipo == 'rosca':
        fig = go.Figure(data=[go.Pie(
            labels=list(dados.keys()),
            values=list(dados.values()),
            hole=hole,
            textinfo="percent+label",
            hoverinfo="label+percent",
            marker=dict(colors=cores)
        )])
    elif tipo == 'barras':
        fig = go.Figure(data=[go.Bar(
            x=list(dados.keys()),
            y=list(dados.values()),
            text=list(dados.values()),
            textposition='auto',
            marker=dict(color=cores)
        )])
    elif tipo == 'treemap':
        fig = px.treemap(
            names=list(dados.keys()),
            values=list(dados.values()),
            title=titulo,
            color=list(dados.values()),
            color_continuous_scale=cores
        )
    
    # Atualizando layout com título e fontes
    fig.update_layout(
        title=titulo,
        title_x=0.5,
        plot_bgcolor="white",
        margin=dict(t=0, b=0, l=0, r=0),
        font=dict(
            family="Arial, sans-serif",
            size=18,
            color="black"
        ),
        title_font=dict(size=24, family="Arial, sans-serif", color="black")
    )

    return fig

def grafico_comparativo(distribuicao_atual, distribuicao_desejada, titulo="Comparação de Distribuições"):
    """
    Função para criar um gráfico de barras comparando a distribuição atual com a distribuição desejada, 
    utilizando cores da biblioteca plotly.
    
    :param distribuicao_atual: Dicionário com os valores atuais dos ativos
    :param distribuicao_desejada: Dicionário com os valores desejados dos ativos
    :param titulo: Título do gráfico
    :return: Gráfico Plotly configurado
    """
    # Obtendo os dados para o gráfico
    ativos = list(distribuicao_atual.keys())
    valores_atual = list(distribuicao_atual.values())
    valores_desejado = list(distribuicao_desejada.values())

    # Usar uma paleta de cores da biblioteca plotly
    cores = px.colors.qualitative.Set2  # Escolhe uma paleta qualitativa do Plotly

    # Criando o gráfico de barras comparativo
    fig = go.Figure(data=[
        go.Bar(
            x=ativos, 
            y=valores_atual, 
            name="Distribuição Atual", 
            marker=dict(color=cores[0])  # Cor para a distribuição atual
        ),
        go.Bar(
            x=ativos, 
            y=valores_desejado, 
            name="Distribuição Desejada", 
            marker=dict(color=cores[1])  # Cor para a distribuição desejada
        )
    ])

    # Atualizando layout
    fig.update_layout(
        title=titulo,
        title_x=0.5,
        barmode='group',  # Barras lado a lado
        xaxis_title="Ativos",
        yaxis_title="Valor (R$)",
        plot_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=20, color="black"),
        legend=dict(font=dict(size=18)),
        xaxis=dict(title="Ativos", tickfont=dict(size=14)),  # Ajusta a fonte dos rótulos do eixo X
        yaxis=dict(title="Valor Investido (R$)", tickfont=dict(size=14)),  # Ajusta a fonte dos rótulos do eixo Y
        title_font=dict(size=24, family="Arial, sans-serif", color="black"),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig

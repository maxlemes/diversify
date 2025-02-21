# src/visualizacao_graficos.py

import matplotlib.pyplot as plt


def grafico_comparativo(
    dados_1,
    dados_2,
    labels=None,
    legenda_1="Série 1",
    legenda_2="Série 2",
    titulo="Gráfico Comparativo",
    xlabel="Categorias",
    ylabel="Valores",
    largura_barra=0.3,
    cor_1="skyblue",
    cor_2="orange",
    rotacao_xticks=45,
    tamanho_figura=(10, 6),
):
    """
    Gera um gráfico de barras comparativo entre duas séries de dados.

    Parâmetros:
        dados_1 (dict): Dados da primeira série, onde as chaves são categorias e os valores são os dados.
        dados_2 (dict): Dados da segunda série, com as mesmas categorias de `dados_1`. Valores ausentes serão considerados 0.
        labels (list, opcional): Lista de rótulos para as categorias. Por padrão, utiliza as chaves de `dados_1`.
        legenda_1 (str): Rótulo da legenda para a primeira série.
        legenda_2 (str): Rótulo da legenda para a segunda série.
        titulo (str): Título do gráfico.
        xlabel (str): Rótulo do eixo x.
        ylabel (str): Rótulo do eixo y.
        largura_barra (float): Largura das barras.
        cor_1 (str): Cor das barras da primeira série.
        cor_2 (str): Cor das barras da segunda série.
        rotacao_xticks (int): Rotação dos rótulos no eixo x.
        tamanho_figura (tuple): Tamanho da figura em polegadas.

    Retorno:
        plt: Objeto Matplotlib para renderização do gráfico.
    """
    if labels is None:
        labels = list(dados_1.keys())
    valores_1 = [dados_1.get(label, 0) for label in labels]
    valores_2 = [dados_2.get(label, 0) for label in labels]

    x = range(len(labels))  # Posicionamento das barras no gráfico

    plt.figure(figsize=tamanho_figura)
    plt.bar(
        x,
        valores_1,
        width=largura_barra,
        label=legenda_1,
        color=cor_1,
        align="center",
    )
    plt.bar(
        [p + largura_barra for p in x],
        valores_2,
        width=largura_barra,
        label=legenda_2,
        color=cor_2,
        align="center",
    )

    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(titulo, fontsize=16)
    plt.xticks([p + largura_barra / 2 for p in x], labels, rotation=rotacao_xticks)
    plt.legend()

    return plt

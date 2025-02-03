import pandas as pd


def ler_dados_csv(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo)
        df.fillna(
            0, inplace=True
        )  # Se houver valores nulos, substituímos por 0
        return df
    except FileNotFoundError:
        return None

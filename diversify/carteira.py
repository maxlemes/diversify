import pandas as pd

# Função para ler o arquivo CSV com os dados de patrimônio
def ler_patrimonio(caminho_arquivo):
    try:
        patrimonio = pd.read_csv(caminho_arquivo)
        return patrimonio
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return None

# Função para calcular os percentuais investidos
def percentuais_atual(patrimonio):
    total_investido = patrimonio['valor'].sum()  # Soma de todos os valores investidos
    percentuais = {}  # Dicionário para armazenar os percentuais

    # Para cada classe de ativo, calcular o percentual
    for index, row in patrimonio.iterrows():
        valor_ativo = row['valor']  # Valor investido no ativo

        # Se o valor do ativo for vazio (NaN), ignore o ativo
        if pd.isna(valor_ativo) or valor_ativo == 0:
        
        percentual = (valor_ativo / total_investido) * 100  # Cálculo do percentual
        percentuais[row['classe_ativo']] = percentual

    return percentuais


# Rodar a função principal
if __name__ == "__main__":
    main()


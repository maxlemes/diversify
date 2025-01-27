import streamlit as st
from src.ler_csv import ler_dados_csv
from src.calculo_percentuais import calcular_percentuais_atuais
from src.visualizacao import grafico_comparativo
import pandas as pd

def main():
    caminho_arquivo = "data/patrimonio.csv"
    
    # Lê o arquivo CSV e calcula os percentuais atuais
    df = ler_dados_csv(caminho_arquivo)
    
    # Percentuais ideais: Lidos pela sidebar
    st.sidebar.title("Percentuais Desejados")

    percentuais_ideais = {
        "renda_fixa": st.sidebar.number_input("Renda Fixa (%)", min_value=0, max_value=100, value=40),
        "acoes": st.sidebar.number_input("Ações (%)", min_value=0, max_value=100, value=30),
        "fundos_previdenciarios": st.sidebar.number_input("Fundos Previdenciários (%)", min_value=0, max_value=100, value=10),
        "criptomoedas": st.sidebar.number_input("Criptomoedas (%)", min_value=0, max_value=100, value=10),
        "fiis": st.sidebar.number_input("FIIs (%)", min_value=0, max_value=100, value=5),
        "renda_exterior": st.sidebar.number_input("Renda no Exterior (%)", min_value=0, max_value=100, value=5)
    }

    # Garantir que os percentuais somem 100
    percentuais_ideais["renda_exterior"] = 100 - sum([v for k, v in percentuais_ideais.items() if k != "renda_exterior"])

    if df is not None:
        percentuais_atuais = calcular_percentuais_atuais(df)

        # Exibição da tabela com os percentuais
        st.title("Distribuição de Investimentos")
        st.write("Percentuais Atuais vs. Ideais:")

        # Criar DataFrame para exibição e formatar os valores
        dados_tabela = pd.DataFrame({
        "Classe de Ativo": percentuais_atuais.keys(),
        "Percentual Atual (%)": [f"{valor:.1f}" for valor in percentuais_atuais.values()],
        "Percentual Ideal (%)": [f"{percentuais_ideais.get(ativo, 0):.1f}" for ativo in percentuais_atuais.keys()]
        })

        # Exibir a tabela
        st.dataframe(dados_tabela)

        # Gerar o gráfico comparativo entre percentuais atuais e ideais
        fig = grafico_comparativo(
            dados_1 = percentuais_atuais,
            dados_2 = percentuais_ideais,
            legenda_1 = 'Atual',
            legenda_2 = 'Ideal',
            titulo = 'Distribuição dos investimentos',
            xlabel = 'Classe de ativos',
            ylabel = 'Percentual (%)',
            cor_1 = 'orange',
            cor_2 = 'blue',
            largura_barra = 0.45
        )
        st.pyplot(fig)

if __name__ == "__main__":
    main()


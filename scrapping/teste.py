from scrapping.raspador import Raspador
from scrapping.tratador import TratadorDeDados
from banco_dados.gerenciador import GerenciadorBanco
from banco_dados.operacoes import OperacoesBanco
import pandas as pd

if __name__ == "__main__":
    banco = GerenciadorBanco()
    operacoes = OperacoesBanco(banco)

    ativo = 'WEGE3'
    tipo_balanco = 'dre'


    # raspador = Raspador(ativo, tipo_balanco, headless=True)

    # tabela_html = raspador.coletar_tabela()
    # if tabela_html:
    #     print("Tabela extraída com sucesso!")
    #     print(tabela_html)  # Exibe a tabela como HTML
    # else:
    #     print("Falha ao extrair a tabela.")

    # # Fechando o navegador
    # raspador.fechar_navegador()

    dados = [['', '', 'Moeda: BRL', '2004\nDez 2004\n2005\nDez 2005\n2006\nDez 2006\n2007\nDez 2007\n2008\nDez 2008\n2009\nDez 2009\n2010\nDez 2010\n2011\nDez 2011\n2012\nDez 2012\n2013\nDez 2013\n2014\nDez 2014\n2015\nDez 2015\n2016\nDez 2016\n2017\nDez 2017\n2018\nDez 2018\n2019\nDez 2019\n2020\nDez 2020\n2021\nDez 2021\n2022\nDez 2022\n2023\nDez 2023\nTTM', ''], ['', '', 'Receita Total', '', '\u202a\u202a13,35\u202fB\u202c\u202c\n+11,51%\n\u202a\u202a17,47\u202fB\u202c\u202c\n+30,88%\n\u202a\u202a23,56\u202fB\u202c\u202c\n+34,88%\n\u202a\u202a29,90\u202fB\u202c\u202c\n+26,91%\n\u202a\u202a32,50\u202fB\u202c\u202c\n+8,69%\n\u202a\u202a35,73\u202fB\u202c\u202c', ''], ['', '', 'Custo das mercadorias vendidas', '', '\u202a\u202a−9,70\u202fB\u202c\u202c\n\u202a\u202a−12,46\u202fB\u202c\u202c\n\u202a\u202a−17,17\u202fB\u202c\u202c\n\u202a\u202a−21,88\u202fB\u202c\u202c\n\u202a\u202a−22,57\u202fB\u202c\u202c\n\u202a\u202a−24,57\u202fB\u202c\u202c', ''], ['', '', 'Lucro Bruto', '', '\u202a\u202a3,65\u202fB\u202c\u202c\n+13,23%\n\u202a\u202a5,01\u202fB\u202c\u202c\n+37,33%\n\u202a\u202a6,39\u202fB\u202c\u202c\n+27,68%\n\u202a\u202a8,03\u202fB\u202c\u202c\n+25,63%\n\u202a\u202a9,94\u202fB\u202c\u202c\n+23,77%\n\u202a\u202a11,16\u202fB\u202c\u202c', ''], ['', '', 'Despesas operacionais (excl. CPV)', '', '\u202a\u202a−1,81\u202fB\u202c\u202c\n\u202a\u202a−2,17\u202fB\u202c\u202c\n\u202a\u202a−2,62\u202fB\u202c\u202c\n\u202a\u202a−3,01\u202fB\u202c\u202c\n\u202a\u202a−3,46\u202fB\u202c\u202c\n\u202a\u202a−3,98\u202fB\u202c\u202c', ''], ['', '', 'Resultado Operacional', '', '\u202a\u202a1,84\u202fB\u202c\u202c\n+21,36%\n\u202a\u202a2,83\u202fB\u202c\u202c\n+54,22%\n\u202a\u202a3,77\u202fB\u202c\u202c\n+33,16%\n\u202a\u202a5,02\u202fB\u202c\u202c\n+33,21%\n\u202a\u202a6,48\u202fB\u202c\u202c\n+28,98%\n\u202a\u202a7,17\u202fB\u202c\u202c', ''], ['', '', 'Receita não operacional, total', '', '\u202a\u202a−42,52\u202fM\u202c\u202c\n\u202a\u202a−89,50\u202fM\u202c\u202c\n\u202a\u202a558,63\u202fM\u202c\u202c\n\u202a\u202a91,60\u202fM\u202c\u202c\n\u202a\u202a110,76\u202fM\u202c\u202c\n\u202a\u202a190,45\u202fM\u202c\u202c', ''], ['', '', 'Receita antes de impostos', '', '\u202a\u202a1,79\u202fB\u202c\u202c\n+20,07%\n\u202a\u202a2,74\u202fB\u202c\u202c\n+52,88%\n\u202a\u202a4,33\u202fB\u202c\u202c\n+57,87%\n\u202a\u202a5,12\u202fB\u202c\u202c\n+18,14%\n\u202a\u202a6,59\u202fB\u202c\u202c\n+28,83%\n\u202a\u202a7,36\u202fB\u202c\u202c', ''], ['', '', 'Equity em resultados', '', '\u202a\u202a10,44\u202fM\u202c\u202c\n\u202a\u202a3,87\u202fM\u202c\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a\u202a113,00\u202fK\u202c\u202c\n\u202a\u202a−921,00\u202fK\u202c\u202c', ''], ['', '', 'Impostos', '', '\u202a\u202a−172,00\u202fM\u202c\u202c\n\u202a\u202a−350,69\u202fM\u202c\u202c\n\u202a\u202a−672,56\u202fM\u202c\u202c\n\u202a\u202a−842,77\u202fM\u202c\u202c\n\u202a\u202a−723,18\u202fM\u202c\u202c\n\u202a\u202a−1,02\u202fB\u202c\u202c', ''], ['', '', 'Participação de não-controladores/minoritários', '', '\u202a\u202a−17,87\u202fM\u202c\u202c\n\u202a\u202a−55,08\u202fM\u202c\u202c\n\u202a\u202a−71,53\u202fM\u202c\u202c\n\u202a\u202a−64,79\u202fM\u202c\u202c\n\u202a\u202a−135,94\u202fM\u202c\u202c\n\u202a\u202a−244,60\u202fM\u202c\u202c', ''], ['', '', 'Depois de impostos outras receitas/despesas', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Lucro líquido antes das operações descontinuadas', '', '\u202a\u202a1,61\u202fB\u202c\u202c\n\u202a\u202a2,34\u202fB\u202c\u202c\n\u202a\u202a3,59\u202fB\u202c\u202c\n\u202a\u202a4,21\u202fB\u202c\u202c\n\u202a\u202a5,73\u202fB\u202c\u202c\n\u202a\u202a6,09\u202fB\u202c\u202c', ''], ['', '', 'Operações descontinuadas', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Lucro Líquido', '', '\u202a\u202a1,61\u202fB\u202c\u202c\n+20,64%\n\u202a\u202a2,34\u202fB\u202c\u202c\n+44,98%\n\u202a\u202a3,59\u202fB\u202c\u202c\n+53,19%\n\u202a\u202a4,21\u202fB\u202c\u202c\n+17,35%\n\u202a\u202a5,73\u202fB\u202c\u202c\n+36,21%\n\u202a\u202a6,09\u202fB\u202c\u202c', ''], ['', '', 'Ajuste de diluição', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Dividendos preferenciais', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Lucro líquido diluído disponível para acionistas ordinários', '', '\u202a\u202a1,61\u202fB\u202c\u202c\n\u202a\u202a2,34\u202fB\u202c\u202c\n\u202a\u202a3,59\u202fB\u202c\u202c\n\u202a\u202a4,21\u202fB\u202c\u202c\n\u202a\u202a5,73\u202fB\u202c\u202c\n\u202a\u202a6,09\u202fB\u202c\u202c', ''], ['', '', 'Lucro básico por ação (EPS Básico)', '', '\u202a0,38\u202c\n+20,63%\n\u202a0,56\u202c\n+44,97%\n\u202a0,85\u202c\n+53,16%\n\u202a1,00\u202c\n+17,35%\n\u202a1,37\u202c\n+36,22%\n\u202a1,45\u202c', ''], ['', '', 'Lucro diluído por ação (EPS Diluído)', '', '\u202a0,38\u202c\n+20,63%\n\u202a0,56\u202c\n+44,97%\n\u202a0,85\u202c\n+53,22%\n\u202a1,00\u202c\n+17,33%\n\u202a1,37\u202c\n+36,23%\n\u202a1,45\u202c', ''], ['', '', 'Média de ações ordinárias em circulação', '', '\u202a\u202a4,19\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n—', ''], ['', '', 'Ações diluídas em circulação', '', '\u202a\u202a4,20\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n\u202a\u202a4,20\u202fB\u202c\u202c\n—', ''], ['', '', 'EBITDA', '', '\u202a\u202a2,23\u202fB\u202c\u202c\n+22,02%\n\u202a\u202a3,28\u202fB\u202c\u202c\n+47,03%\n\u202a\u202a4,29\u202fB\u202c\u202c\n+30,70%\n\u202a\u202a5,59\u202fB\u202c\u202c\n+30,25%\n\u202a\u202a7,11\u202fB\u202c\u202c\n+27,16%\n\u202a\u202a7,91\u202fB\u202c\u202c', ''], ['', '', 'EBIT', '', '\u202a\u202a1,84\u202fB\u202c\u202c\n+21,36%\n\u202a\u202a2,83\u202fB\u202c\u202c\n+54,22%\n\u202a\u202a3,77\u202fB\u202c\u202c\n+33,16%\n\u202a\u202a5,02\u202fB\u202c\u202c\n+33,21%\n\u202a\u202a6,48\u202fB\u202c\u202c\n+28,98%\n\u202a\u202a7,17\u202fB\u202c\u202c', ''], ['', '', 'Total de custos operacionais', '', '\u202a\u202a−11,51\u202fB\u202c\u202c\n\u202a\u202a−14,64\u202fB\u202c\u202c\n\u202a\u202a−19,79\u202fB\u202c\u202c\n\u202a\u202a−24,88\u202fB\u202c\u202c\n\u202a\u202a−26,02\u202fB\u202c\u202c\n\u202a\u202a−28,55\u202fB\u202c\u202c', '']]

    if dados:
        # Criar o tratador de dados
        tratador = TratadorDeDados(ativo, dados)
        
        # Criar o DataFrame com os dados tratados
        df = tratador.criar_dataframe()
        print(df)
        
        # # Exibir os dados tratados
        # if df_tratado is not None:
        #     print(df_tratado)
        #     print(df_tratado.columns)
        # else:
        #     print("Erro ao tratar os dados.")
    
    operacoes.inserir_dataframe(tipo_balanco, df)


    dados_financeiros = operacoes.consultar_financas("dre", 'WEGE3')
    colunas = operacoes.listar_colunas('dre')
    
    # Converter para DataFrame
    dt = pd.DataFrame(dados_financeiros, columns=colunas).sort_values(by='id')
    # Mostrar o DataFrame
    print(dt)

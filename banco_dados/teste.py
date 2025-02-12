# Importando as classes que você criou
from banco_dados.gerenciador import GerenciadorBanco
from banco_dados.operacoes import OperacoesBanco

if __name__ == "__main__":
    banco = GerenciadorBanco()
    operacoes = OperacoesBanco(banco)

    # Inserindo um perfil
    operacoes.inserir_perfil(
        "WEG S.A.", 
        "WEGE3", 
        "Bens de Capital", 
        "Máquinas e Equipamentos",
        "A WEG é uma multinacional brasileira que fabrica equipamentos eletroeletrônicos, "
        "como motores elétricos, geradores e transformadores."
    )

    # Consultando perfil
    perfil = operacoes.consultar_perfil("WEGE3")
    if perfil:
        print(f"Perfil encontrado: {perfil}")

    # Inserindo dados financeiros
    anos_exemplo = {2019: -1.3, 2020: 5.21, 2021: 24.19, 2022: 20.68, 2023: 9.15}
    operacoes.inserir_financas("dre", 'VALE3', 'Lucro básico por ação (EPS Básico)', -349391.6232885078, 11.27, anos_exemplo)
  
    # # Consultando dados financeiros
    # dados_financeiros = operacoes.consultar_financas("dre", 'VALE3', 'Lucro básico por ação (EPS Básico)')
    # if dados_financeiros:
    #     for dado in dados_financeiros:
    #         print(dado)

    # Atualizar dados financeiros para o ativo 'VALE3' com um novo ano (2024)
    anos_exemplo = {2019: -1.3, '2020': 5.21, '2021': 24.19, '2022': 20.68, '2023': 9.15, '2024': 10.5}
    operacoes.inserir_financas("dre", 'VALE3', 'Lucro básico por ação (EPS Básico)', 123456, 15.01, anos_exemplo)
    
    # operacoes.remover_financas('dre', 'VALE3', 'Lucro básico por ação (EPS Básico)', -349391.6232885078)
    
    # Consultando dados financeiros
    colunas = operacoes.listar_colunas('dre')
    print(colunas)

    dados_financeiros = operacoes.consultar_financas("dre", 'VALE3', 'Lucro básico por ação (EPS Básico)')
    print(dados_financeiros)

    banco.fechar_conexao()

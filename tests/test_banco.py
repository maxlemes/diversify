import pytest
from database.gerenciador import GerenciadorBanco
from database.operacoes import OperacoesBanco


@pytest.fixture
def setup_banco():
    # Configuração inicial do banco
    banco = GerenciadorBanco()
    operacoes = OperacoesBanco(banco)

    # Criação de um perfil e dados financeiros para testar
    operacoes.inserir_perfil(
        "WEG S.A.",
        "WEGE3",
        "Bens de Capital",
        "Máquinas e Equipamentos",
        "A WEG é uma multinacional brasileira que fabrica equipamentos eletroeletrônicos, "
        "como motores elétricos, geradores e transformadores.",
    )

    anos_exemplo = {2019: -1.3, 2020: 5.21, 2021: 24.19, 2022: 20.68, 2023: 9.15}
    operacoes.inserir_financas(
        "dre",
        "VALE3",
        "Lucro básico por ação (EPS Básico)",
        -349391.6232885078,
        11.27,
        anos_exemplo,
    )

    # Retorna a instância da operação para os testes
    yield operacoes

    # Finalização do banco após os testes
    banco.fechar_conexao()


def test_inserir_perfil(setup_banco):
    operacoes = setup_banco
    perfil = operacoes.consultar_perfil("WEGE3")
    assert perfil, "Perfil não encontrado"
    assert (
        perfil["nome"] == "WEG S.A."
    ), f"Esperado 'WEG S.A.', mas obtido {perfil['nome']}"


def test_inserir_financas(setup_banco):
    operacoes = setup_banco
    # Verificar se os dados financeiros foram inseridos corretamente
    dados_financeiros = operacoes.consultar_financas(
        "dre", "VALE3", "Lucro básico por ação (EPS Básico)"
    )
    assert dados_financeiros, "Dados financeiros não encontrados"
    assert (
        dados_financeiros[2] == -349391.6232885078
    ), f"Esperado -349391.6232885078, mas obtido {dados_financeiros[0][2]}"


def test_atualizar_financas(setup_banco):
    operacoes = setup_banco
    # Atualizar dados financeiros para o ativo 'VALE3' com um novo ano (2024)
    anos_exemplo = {
        2019: -1.3,
        2020: 5.21,
        2021: 24.19,
        2022: 20.68,
        2023: 9.15,
        2024: 10.5,
    }
    operacoes.inserir_financas(
        "dre",
        "VALE3",
        "Lucro básico por ação (EPS Básico)",
        123456,
        15.01,
        anos_exemplo,
    )

    dados_financeiros = operacoes.consultar_financas(
        "dre", "VALE3", "Lucro básico por ação (EPS Básico)"
    )
    assert dados_financeiros, "Dados financeiros não encontrados após atualização"
    assert (
        dados_financeiros[2] == 123456
    ), f"Esperado 123456, mas obtido {dados_financeiros[0][2]}"


def test_listar_colunas(setup_banco):
    operacoes = setup_banco
    colunas = operacoes.listar_colunas("dre")
    assert colunas, "Não foi possível listar as colunas"
    assert isinstance(colunas, list), "Esperado um tipo de dado 'list' para as colunas"
    assert "ativo" in colunas, "A coluna 'ativo' não foi encontrada nas colunas"

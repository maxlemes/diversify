# ==============================================================================
# DIVERSIFY/DIVERSIFY/SERVICES.PY
# ==============================================================================
#
# DESCRIÇÃO:
# Este arquivo representa a "Camada de Serviço" (Service Layer) da aplicação.
# É aqui que reside a lógica de negócio principal. A classe `PortfolioService`
# atua como um orquestrador, utilizando os Repositórios (a camada de acesso a
# dados) para buscar e salvar informações, e então aplicando regras de negócio
# e cálculos complexos sobre esses dados.
#
# ARQUITETURA:
# A `PortfolioService` é o intermediário entre a camada de apresentação
# (ex: a interface do usuário, os scripts em `tasks/`) e a camada de dados
# (`repositories.py`). Ela desacopla a lógica de negócio dos detalhes de
# implementação do banco de dados. Por exemplo, um script de tarefa não precisa
# saber como calcular o "Risk Parity", ele simplesmente chama o método
# correspondente no serviço.
#
# PRINCIPAIS RESPONSABILIDADES:
#
# 1. Orquestração de Repositórios:
#    - Combina as funcionalidades de múltiplos repositórios para executar
#      operações complexas, como `adicionar_transacao_completa`, que envolve
#      tanto `AtivoRepository` quanto `TransacaoRepository`.
#
# 2. Lógica de Negócio e Cálculos Financeiros:
#    - Contém a "inteligência" da aplicação. É responsável por calcular a
#      posição atual da carteira, o valor de mercado, a volatilidade dos
#      ativos e implementar estratégias como o "Risk Parity".
#
# 3. Geração de Planos e Análises:
#    - Cria recomendações acionáveis, como planos de rebalanceamento
#      (`gerar_plano_rebalanceamento...`) e de novos aportes
#      (`gerar_plano_de_aporte`).
#
# 4. Transformação de Dados:
#    - Utiliza extensivamente a biblioteca Pandas para converter os dados brutos
#      do banco de dados em estruturas (DataFrames) adequadas para análise
#      matemática e estatística.
#
# COMPONENTES:
# - PosicaoAtivo (Dataclass): Uma estrutura de dados simples para representar
#   a posição consolidada de um ativo, facilitando o tráfego de informações
#   entre os métodos.
# - PortfolioService: A classe principal que encapsula todos os métodos de
#   serviço relacionados à gestão e análise de portfólios.
#
# ==============================================================================


# Dependências da nossa aplicação
from db_nexus import DatabaseSessionManager

from .repositories import (
    AtivoRepository,
    CarteiraRepository,
    DadoHistoricoRepository,
    TransacaoRepository,
)


class PortfolioService:
    """
    Orquestra as operações relacionadas à análise de portfólio.
    Esta é a camada de lógica de negócio.
    """

    def __init__(self, session_manager: DatabaseSessionManager):
        # Injeção de Dependência: o serviço recebe o gerenciador de sessão.
        self.session_manager = session_manager
        # O serviço instancia os repositórios que ele precisa.
        self.ativo_repo = AtivoRepository()
        self.transacao_repo = TransacaoRepository()
        self.dado_historico_repo = DadoHistoricoRepository()
        self.carteira_repo = CarteiraRepository()

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

from typing import List, Tuple

from db_nexus import DatabaseSessionManager

from .models import TipoAtivo
from .repositories import AtivoRepository


class AtivoService:
    """
    Contém a lógica de negócio de alto nível para lidar com a classe ATIVO.
    """

    def __init__(self, session_manager: DatabaseSessionManager):
        self.session_manager = session_manager
        self.ativo_repo = AtivoRepository()

    def populate_assets(
        self,
        composition_data: list[dict],
        db_manager: DatabaseSessionManager,
        tipo: TipoAtivo,
    ):
        """
        Recebe dados de composição e popula a tabela 'ativos' no banco de dados.
        """
        print("\n--- Populando/Atualizando tabela de ativos ---")
        ativo_repo = AtivoRepository()
        created_or_updated_assets = []

        with db_manager.get_session() as session:
            for asset_info in composition_data:
                ticker = asset_info["ticker"]
                nome = asset_info["nome"]

                # 2. Usa o repositório para buscar ou criar o ativo
                ativo = ativo_repo.find_or_create(session, ticker, nome, tipo)
                created_or_updated_assets.append(ativo)

        print(
            f"--- Tabela de ativos populada/atualizada com {len(created_or_updated_assets)} registros. ---"
        )

    def get_all_asset_ids_and_tickers(self) -> List[Tuple[int, str]]:
        """
        Orquestra a busca por IDs e tickers de todos os ativos.

        Gerencia a sessão do banco de dados, garantindo que a conexão
        seja aberta e fechada corretamente.
        """
        print("Serviço solicitado para buscar IDs e Tickers.")
        # O 'with' statement do seu db_nexus cuida de TUDO:
        # 1. Abre a conexão e inicia a sessão.
        # 2. Executa o código dentro do bloco.
        # 3. Se tudo der certo, ele fecha a sessão e a conexão.
        # 4. Se ocorrer um erro, ele desfaz a transação (rollback) e DEPOIS fecha tudo.
        with self.session_manager.get_session() as session:
            # Delega a busca ao repositório, que sabe como falar com o banco
            lista_de_ativos = self.ativo_repo.list_all_ids_and_tickers(session)
            print(f"Encontrados {len(lista_de_ativos)} ativos.")
            return lista_de_ativos

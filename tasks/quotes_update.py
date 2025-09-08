import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para encontrar o pacote 'diversify'
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db_nexus.base import Base
from db_nexus.session import DatabaseSessionManager

from diversify.quotes_services import QuoteService


def main():
    """Script principal para atualizar as cotações históricas."""
    print("==========================================================")
    print("🚀 INICIANDO SCRIPT DE ATUALIZAÇÃO DE COTAÇÕES")
    print("==========================================================")

    db_manager = DatabaseSessionManager("sqlite:///diversify.db")
    quote_service = QuoteService()

    # Garante que as tabelas do banco de dados existam
    db_manager.create_all_tables()

    # Chama o serviço que faz todo o trabalho pesado.
    quote_service.update_historical_prices(db_manager)

    print("\n==========================================================")
    print("🏁 SCRIPT DE ATUALIZAÇÃO DE COTAÇÕES FINALIZADO.")
    print("==========================================================")


if __name__ == "__main__":
    main()

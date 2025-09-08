import json
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para encontrar o pacote 'diversify'
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importa as ferramentas de banco de dados
from db_nexus.session import DatabaseSessionManager

from diversify.b3_services import B3Service
from diversify.database import models
from diversify.database.services import AtivoService


def main():
    """
    Script para ler os dados processados dos arquivos JSON e inseri-los no banco de dados.
    """
    print("==========================================================")
    print("🚀 INICIANDO SCRIPT DE INSERÇÃO NO BANCO DE DADOS")
    print("==========================================================")

    # --- 0. ATUALIZANDO OS ÍNDICES DA B3, CASO NECESSÁRIO
    b3_service = B3Service()
    b3_service.refresh_index()

    # --- 1. INICIALIZAÇÃO DO BANCO DE DADOS ---
    print("Inicializando o gerenciador de banco de dados...")
    db_manager = DatabaseSessionManager("sqlite:///diversify.db")
    ativo_service = AtivoService(session_manager=db_manager)

    # Garante que os modelos sejam "conhecidos" pelo SQLAlchemy antes de criar as tabelas
    db_manager.create_all_tables()

    # --- 2. LER OS DADOS DOS ARQUIVOS JSON ---
    processed_data_dir = Path("processed_data")
    if not processed_data_dir.exists():
        print(
            f"❌ ERRO: O diretório '{processed_data_dir}' não foi encontrado. Execute o refresh primeiro."
        )
        return

    json_files = list(processed_data_dir.glob("*_composition.json"))
    if not json_files:
        print("Nenhum arquivo JSON de composição encontrado para processar.")
        return

    # --- MAPEAMENTO DE ÍNDICE PARA TIPO DE ATIVO ---
    INDEX_TO_ASSET_TYPE_MAP = {
        "IFIX": models.TipoAtivo.FII,
        "FIAGROS": models.TipoAtivo.FIAGRO,  # Chave para sua lista de Fiagros
        "FIINFRAS": models.TipoAtivo.FIINFRA,  # Índice oficial de FI-Infra
        "INDEX": models.TipoAtivo.INDICE,
    }
    DEFAULT_ASSET_TYPE = models.TipoAtivo.ACAO

    # --- 3. INSERIR OS DADOS NO BANCO ---
    for json_file in json_files:

        # Extrai o nome do índice do nome do arquivo (ex: "IFIX_composition.json" -> "IFIX")
        index_name = json_file.stem.replace("_composition", "")
        tipo = INDEX_TO_ASSET_TYPE_MAP.get(index_name, DEFAULT_ASSET_TYPE)

        print(f"\nLendo dados do arquivo: {json_file.name}")
        with open(json_file, "r", encoding="utf-8") as f:
            composition_data = json.load(f)

        if composition_data:
            # Primeiro, popula a tabela de ativos
            ativo_service.populate_assets(composition_data, db_manager, tipo)

        else:
            print(f"⚠️ Arquivo para '{index_name}' está vazio. Pulando inserção no DB.")

    print("\n==========================================================")
    print("🏁 SCRIPT DE INSERÇÃO FINALIZADO.")
    print("==========================================================")


if __name__ == "__main__":
    main()

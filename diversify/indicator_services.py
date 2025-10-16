import datetime as dt

import numpy as np
import pandas as pd

from diversify.database.models import Indicador
from diversify.database.repositories import (
    AtivoRepository,
    IndicatorRepository,
    PrecoHistoricoRepository,
)


class IndicatorService:
    """
    Serviço responsável por calcular e atualizar indicadores financeiros
    e de risco (ex: volatilidade, P/L, P/VP etc.) com base em dados já
    armazenados no banco de dados.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.ativo_repo = AtivoRepository()
        self.preco_repo = PrecoHistoricoRepository()
        self.indicador_repo = IndicatorRepository()

    # ==========================================================
    # 📈 CÁLCULO DA VOLATILIDADE DE 2 ANOS
    # ==========================================================
    def calcular_volatilidade_2a(self):
        print("\n--- Calculando volatilidade de 2 anos (Otimizado) ---")
        hoje = dt.date.today()
        dois_anos_atras = hoje - dt.timedelta(days=2 * 365)

        with self.db_manager.get_session() as session:
            # 1. Busca todos os dados de uma vez
            todos_precos = self.preco_repo.get_all_prices_since(
                session, start_date=dois_anos_atras
            )

            if not todos_precos:
                print("Nenhum preço encontrado nos últimos 2 anos.")
                return

            # 2. Constrói um DataFrame a partir dos objetos ORM
            rows = [
                {
                    "ativo_id": p.ativo_id,
                    "data_pregao": p.data_pregao,
                    "preco_fechamento": p.preco_fechamento,
                    "retorno": getattr(p, "retorno", None),
                }
                for p in todos_precos
            ]
            df_total = pd.DataFrame(rows)
            if df_total.empty:
                print("Nenhum preço válido após conversão para DataFrame.")
                return

            indicadores_para_salvar = []

            # 3. Agrupa por ativo e calcula
            for ativo_id, df_ativo in df_total.groupby("ativo_id"):
                df_ativo = df_ativo.sort_values("data_pregao")

                # Se o campo 'retorno' não estiver preenchido, calcula a partir do fechamento
                if "retorno" not in df_ativo.columns or df_ativo["retorno"].isna().all():
                    df_ativo["retorno"] = df_ativo["preco_fechamento"].pct_change()

                df_ativo = df_ativo.dropna(subset=["retorno"])

                if len(df_ativo) < 30:
                    print(f"[{ativo_id}] Poucos dados ({len(df_ativo)} dias). Pulando.")
                    continue

                # Volatilidade anualizada (252 pregões/ano). Usa ddof=1 (amostral).
                vol_2a = float(df_ativo["retorno"].std(ddof=1) * np.sqrt(252))

                # Persiste usando o repositório (método existente inserir_ou_atualizar)
                self.indicador_repo.inserir_ou_atualizar(
                    session=session,
                    ativo_id=int(ativo_id),
                    data_ref=hoje,
                    volatilidade_2a=vol_2a,
                )
                print(f"[{ativo_id}] Volatilidade 2a: {vol_2a:.6f}")

        print("\n✅ Cálculo de volatilidade finalizado e salvo no banco.")

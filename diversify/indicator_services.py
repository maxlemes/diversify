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
        """
        Calcula a volatilidade anualizada (2 anos) para cada ativo,
        usando apenas os preços armazenados no banco.
        """
        print("\n--- Calculando volatilidade de 2 anos ---")

        hoje = dt.date.today()
        dois_anos_atras = hoje - dt.timedelta(days=2 * 365)

        with self.db_manager.get_session() as session:
            ativos = self.ativo_repo.list_all(session)
            print(f"Foram encontrados {len(ativos)} ativos para cálculo.")

            for ativo in ativos:
                precos = self.preco_repo.get_prices_since(ativo.id, dois_anos_atras)

                if not precos:
                    print(f"[{ativo.ticker}] Sem preços nos últimos 2 anos. Pulando.")
                    continue

                # Cria DataFrame com os preços do ativo
                df = pd.DataFrame(precos, columns=["data_pregao", "preco_fechamento"])
                df.sort_values("data_pregao", inplace=True)
                df["retorno"] = df["preco_fechamento"].pct_change()
                df.dropna(inplace=True)

                if len(df) < 30:
                    print(f"[{ativo.ticker}] Poucos dados ({len(df)} dias). Pulando.")
                    continue

                # Volatilidade anualizada (252 pregões/ano)
                vol_2a = np.std(df["retorno"]) * np.sqrt(252)

                indicador = Indicador(
                    ativo_id=ativo.id,
                    data_referencia=hoje,
                    volatilidade_2a=float(vol_2a),
                )

                self.indicador_repo.upsert(session, indicador)
                print(f"[{ativo.ticker}] Volatilidade 2a: {vol_2a:.4f}")

        print("\n✅ Cálculo de volatilidade finalizado e salvo no banco.")

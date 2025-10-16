from datetime import date, timedelta

import pandas as pd
from sqlalchemy.orm import Session

from diversify.database.models import Ativo, PrecoHistorico
from diversify.database.repositories import IndicatorRepository


class IndicadoresService:
    """
    Calcula indicadores como volatilidade, P/L, etc.
    """

    def __init__(self, session: Session):
        self.session = session
        self.repo = IndicatorRepository(session)

    def calcular_volatilidade_2a(self):
        """
        Calcula a volatilidade anualizada (2 anos) de cada ativo
        e grava o resultado na tabela indicadores.
        """
        hoje = date.today()
        inicio_periodo = hoje - timedelta(days=2 * 365)

        ativos = self.session.query(Ativo).all()
        for ativo in ativos:
            precos = (
                self.session.query(PrecoHistorico)
                .filter(
                    PrecoHistorico.ativo_id == ativo.id,
                    PrecoHistorico.data_pregao >= inicio_periodo,
                )
                .order_by(PrecoHistorico.data_pregao)
                .all()
            )

            if len(precos) < 60:  # evita ativos sem histórico suficiente
                continue

            df = pd.DataFrame(
                [(p.data_pregao, p.preco_fechamento) for p in precos],
                columns=["data", "fechamento"],
            )
            df["retorno"] = df["fechamento"].pct_change()

            vol_diaria = df["retorno"].std()
            vol_anualizada = vol_diaria * (252**0.5)  # 252 pregões por ano

            self.repo.inserir_ou_atualizar(
                ativo_id=ativo.id,
                data_ref=hoje,
                volatilidade_2a=round(float(vol_anualizada), 4),
            )

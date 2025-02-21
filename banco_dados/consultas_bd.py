import logging

from banco_dados.conexao_bd import ConexaoBD

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ConsultasBD:
    def __init__(self, banco_dados):
        """
        Construtor da classe ConsultasBD.

        Parâmetros:
            banco_dados (ConexaoBD): Instância da classe ConexaoBD para interagir com o banco de dados.
        """
        self.bd = banco_dados

    def _executar_consulta(self, query, parametros=None):
        """
        Executa uma consulta SQL no banco de dados.

        Parâmetros:
            query (str): Comando SQL para consulta.
            parametros (tuple, opcional): Parâmetros da consulta.

        Retorna:
            list: Lista de tuplas com os resultados da consulta.
        """
        try:
            cursor = self.bd.cursor
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Erro ao consultar dados: {e}")
            return []

    def listar_tabelas(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        return [t[0] for t in self._executar_consulta(query)]

    def consultar_tabelas(self, tabela, coluna):
        query = f"SELECT DISTINCT {coluna} FROM {tabela} ORDER BY {coluna};"
        return [t[0] for t in self._executar_consulta(query)]

    def buscar_perfil(self, nome=None, ticker=None, setor=None, subsetor=None):
        """
        Busca registros na tabela 'perfil' com base nos filtros fornecidos.

        Parâmetros:
            nome (str, opcional): Nome da empresa.
            ticker (str, opcional): Código do ativo.
            setor (str, opcional): Setor da empresa.
            subsetor (str, opcional): Subsetor da empresa.

        Retorna:
            list: Lista de tuplas com os resultados encontrados.
        """
        query = "SELECT * FROM perfil WHERE 1=1"
        parametros = []

        if nome:
            query += " AND nome LIKE ?"
            parametros.append(f"%{nome}%")
        if ticker:
            query += " AND ticker = ?"
            parametros.append(ticker)
        if setor:
            query += " AND setor LIKE ?"
            parametros.append(f"%{setor}%")
        if subsetor:
            query += " AND subsetor LIKE ?"
            parametros.append(f"%{subsetor}%")

        perfil = self._executar_consulta(query, tuple(parametros))

        if perfil:
            colunas = [
                "id",
                "nome",
                "ticker",
                "setor",
                "subsetor",
                "website",
                "descricao",
            ]
            resultado = dict(zip(colunas, perfil[0]))
        else:
            None

        return resultado

    def buscar_perfil_id(self, ticker):
        """
        Busca o perfil_id de um ativo baseado no ticker.

        Parâmetros:
            ticker (str): Código do ativo.

        Retorna:
            int | None: O perfil_id correspondente ou None se não encontrado.
        """
        try:
            query = "SELECT id FROM perfil WHERE ticker = ?;"
            resultado = self._executar_consulta(query, (ticker,))

            if resultado:
                return resultado[0][0]  # Retorna o perfil_id encontrado
            else:
                logging.warning(f"Ticker '{ticker}' não encontrado na tabela 'perfil'.")
                return None

        except Exception as e:
            logging.error(f"Erro ao buscar perfil_id para {ticker}: {e}")
            return None

    def buscar_cotacoes(self, ticker):
        """
        Consulta as cotações de uma empresa com base no ticker informado.

        Parâmetros:
            ticker (str): O ticker da empresa a ser consultada.

        Retorna:
            list[dict]: Lista de dicionários contendo as cotações da empresa.
        """
        query = """
            SELECT c.*
            FROM cotacoes c
            JOIN perfil p ON c.perfil_id = p.id
            WHERE p.ticker = ?;
        """
        resultado = self._executar_consulta(query, (ticker,))

        # Convertendo para lista de dicionários
        colunas = [
            "perfil_id",
            "data",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
        return [dict(zip(colunas, linha)) for linha in resultado]

    def buscar_dre(self, ticker):
        """
        Consulta os dados da Demonstração do Resultado do Exercício (DRE) de uma empresa com base no ticker informado.

        Parâmetros:
            ticker (str): O ticker da empresa a ser consultada.

        Retorna:
            list[dict]: Lista de dicionários contendo os dados da DRE da empresa.
        """
        query = """
            SELECT d.*
            FROM dre d
            JOIN perfil p ON d.perfil_id = p.id
            WHERE p.ticker = ?;
        """
        resultado = self._executar_consulta(query, (ticker,))

        # Definir os nomes das colunas conforme a estrutura da tabela dre
        colunas = [
            "perfil_id",
            "ano",
            "receita_total",
            "custo_receita",
            "lucro_bruto",
            "despesa_operacional",
            "lucro_operacional",
            "lucro_antes_impostos",
            "provisao_impostos",
            "lucro_liquido",
            "eps_basico",
            "despesas_totais",
            "lucro_normalizado",
            "juros_recebidos",
            "juros_pagos",
            "lucro_juros",
            "ebit",
            "ebitda",
            "depreciacao",
            "ebitda_normalizado",
        ]

        return [dict(zip(colunas, linha)) for linha in resultado]


# Exemplo de uso
if __name__ == "__main__":
    with ConexaoBD() as bd:
        consultas = ConsultasBD(bd)
        resultado = consultas.buscar_perfil(nome="Petrobras")
        print(resultado)

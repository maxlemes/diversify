import logging
import sqlite3
import traceback

from banco_dados.conexao_bd import ConexaoBD

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GerenciadorBD:
    def __init__(self, banco_dados):
        self.bd = banco_dados

    def _buscar_perfil_id(self, ticker):
        """Busca o perfil_id na tabela perfil para um único ticker."""
        query = "SELECT id FROM perfil WHERE ticker = ?"
        resultado = self.bd.cursor.execute(query, (ticker,)).fetchone()
        return resultado[0] if resultado else None

    def tabela_existe(self, nome_tabela):
        """Verifica se uma tabela existe no banco de dados."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        resultado = self.bd.cursor.execute(query, (nome_tabela,)).fetchone()
        return resultado is not None

    def coluna_existe(self, nome_tabela, nome_coluna):
        """Verifica se uma coluna existe em uma tabela no banco de dados."""
        query = "PRAGMA table_info(?);"
        resultado = self.bd.cursor.execute(query, (nome_tabela,)).fetchall()

        # Verifica se a coluna está presente nos resultados
        for coluna in resultado:
            if coluna[1] == nome_coluna:
                return True
        return False

    def dado_existe(self, tabela, perfil_id, ano, coluna):
        """
        Verifica se o valor da coluna especificada é NULL para o registro dado (perfil_id, ano).
        Retorna True se o valor for NULL, caso contrário, False.
        """
        # Consulta para verificar o valor da coluna
        self.bd.cursor.execute(
            f"SELECT {coluna} FROM {tabela} WHERE perfil_id = ? AND ano = ?",
            (perfil_id, ano),
        )
        resultado = self.cursor.fetchone()

        if resultado is None:
            # Se não houver resultado, retorna False
            print(f"Registro com perfil_id {perfil_id} e ano {ano} não encontrado.")
            return False

        valor_coluna = resultado[0]

        # Retorna True se o valor da coluna for NULL, False caso contrário
        return valor_coluna is None

    def criar_tabela(self, nome_tabela, colunas):
        """Cria uma tabela caso ainda não exista."""
        if self.tabela_existe(nome_tabela):
            logging.debug(f"Tabela {nome_tabela} já existe.")
            return
        try:
            colunas_sql = ", ".join(
                [f"{coluna} {tipo}" for coluna, tipo in colunas.items()]
            )
            query = f"CREATE TABLE {nome_tabela} ({colunas_sql});"
            self.bd.executar_query(query)
            logging.debug(f"Tabela {nome_tabela} criada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao criar tabela {nome_tabela}: {e}")
            logging.debug(traceback.format_exc())

    def deletar_tabela(self, nome_tabela):
        """Deleta uma tabela caso ela exista."""
        if not self.tabela_existe(nome_tabela):
            logging.debug(f"Tabela {nome_tabela} não existe.")
            return

        try:
            query = f"DROP TABLE {nome_tabela};"
            self.bd.executar_query(query)
            logging.debug(f"Tabela {nome_tabela} deletada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao deletar tabela {nome_tabela}: {e}")
            logging.debug(traceback.format_exc())

    def adicionar_coluna(self, nome_tabela, nome_coluna, tipo_coluna):
        """Adiciona uma coluna a uma tabela existente."""
        if self.coluna_existe(nome_tabela, nome_coluna):
            logging.debug(f"A coluna {nome_coluna} já existe na tabela {nome_tabela}.")
            return

        try:
            query = f"ALTER TABLE {nome_tabela} ADD COLUMN {nome_coluna} {tipo_coluna};"
            self.bd.executar_query(query)
            logging.debug(
                f"Coluna {nome_coluna} adicionada com sucesso na tabela {nome_tabela}."
            )
        except Exception as e:
            logging.error(
                f"Erro ao adicionar coluna {nome_coluna} na tabela {nome_tabela}: {e}"
            )
            logging.debug(traceback.format_exc())

    def inserir_dados(self, tabela, dados):
        """Insere dados em uma tabela."""
        if not dados:
            logging.warning("Nenhum dado fornecido para inserção.")
            return
        try:

            if tabela in ["cotacoes", "dre", "bp", "fc", "stats"]:
                # Pega o ticker do primeiro dicionário
                ticker = dados[0].get("ticker")
                if not ticker:
                    logging.warning("Nenhum ticker encontrado nos dados.")
                    return

                # Busca o perfil_id correspondente
                perfil_id = self._buscar_perfil_id(ticker)
                if perfil_id is None:
                    logging.warning(f"Ticker {ticker} não encontrado na tabela perfil.")
                    return  # Não insere se não encontrar o perfil_id

                # Adiciona perfil_id em todos os dicionários e remove o ticker
                dados.remove({"ticker": ticker})

                for dado in dados:
                    dado["perfil_id"] = perfil_id

            colunas = list(dados[0].keys())
            placeholders = ", ".join([f":{col}" for col in colunas])
            query = (
                f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"
            )
            self.bd.cursor.executemany(query, dados)
            self.bd.commit()
            logging.debug(f"Dados inseridos na tabela {tabela} com sucesso.")

        except sqlite3.IntegrityError as e:
            logging.error(f"Erro de integridade ao inserir dados: {e}")
            self.bd.rollback()
        except Exception as e:
            logging.error(f"Erro ao inserir dados na tabela {tabela}: {e}")
            logging.debug(traceback.format_exc())
            self.bd.rollback()

    import sqlite3

    def insert_stats(self, tabela, colunas, dados):
        """
        Função genérica para inserir dados em qualquer tabela do banco de dados.

        Parâmetros:
        conn (sqlite3.Connection): Conexão ao banco de dados.
        tabela (str): Nome da tabela onde os dados serão inseridos.
        colunas (list): Lista com os nomes das colunas da tabela.
        dados (list of tuples): Lista de tuplas com os dados a serem inseridos.
        """
        try:
            # Criar a parte do comando SQL para colunas e valores
            colunas_str = ", ".join(colunas)
            placeholders = ", ".join(["?" for _ in colunas])

            # Construir a parte de atualização caso haja conflito
            update_str = ", ".join([f"{coluna} = ?" for coluna in colunas])

            # Comando SQL para inserção
            query = f"""
                INSERT INTO {tabela} ({colunas_str})
                VALUES ({placeholders})
                ON CONFLICT(perfil_id, ano) DO UPDATE SET {update_str};
                """
            # Inserir os dados
            for dado in dados:
                self.bd.cursor.execute(query, dado + dado)

            # Confirmar as mudanças
            self.bd.conn.commit()
            print(f"Dados inseridos com sucesso na tabela {tabela}!")
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados na tabela {tabela}: {e}")

    def tabelas_iniciais(self):
        """Cria as tabelas iniciais."""
        tabelas = {
            "perfil": {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "nome": "TEXT NOT NULL",
                "ticker": "TEXT UNIQUE NOT NULL",
                "setor": "TEXT",
                "subsetor": "TEXT",
                "website": "TEXT",
                "descricao": "TEXT",
            },
            "cotacoes": {
                "perfil_id": "INTEGER",
                "data": "TEXT NOT NULL",
                "open": "REAL",
                "high": "REAL",
                "low": "REAL",
                "close": "REAL",
                "adj_close": "REAL",
                "volume": "INTEGER",
                "PRIMARY KEY": "(perfil_id, data)",
                "FOREIGN KEY": "(perfil_id) REFERENCES perfil(id) ON DELETE CASCADE",
            },
            "dre": {
                "perfil_id": "INTEGER",
                "ano": "INTEGER NOT NULL",
                "receita_total": "REAL",
                "custo_receita": "REAL",
                "lucro_bruto": "REAL",
                "despesa_operacional": "REAL",
                "lucro_operacional": "REAL",
                "lucro_antes_impostos": "REAL",
                "provisao_impostos": "REAL",
                "lucro_liquido": "REAL",
                "eps": "REAL",
                "despesas_totais": "REAL",
                "lucro_normalizado": "REAL",
                "juros_recebidos": "REAL",
                "juros_pagos": "REAL",
                "lucro_juros": "REAL",
                "ebit": "REAL",
                "ebitda": "REAL",
                "depreciacao": "REAL",
                "ebitda_normalizado": "REAL",
                "PRIMARY KEY": "(perfil_id, ano)",
                "FOREIGN KEY": "(perfil_id) REFERENCES perfil(id) ON DELETE CASCADE",
            },
            "bp": {
                "perfil_id": "INTEGER",
                "ano": "INTEGER NOT NULL",
                "caixa_equivalentes_caixa": "REAL",
                "ativo_circulante": "REAL",
                "goodwill_ativos_intangiveis": "REAL",
                "investimentos_longo_prazo": "REAL",
                "ativo_nao_circulante": "REAL",
                "ativos_totais": "REAL",
                "dividendos_a_pagar": "REAL",
                "divida_curto_prazo": "REAL",
                "passivos_curto_prazo": "REAL",
                "divida_longo_prazo": "REAL",
                "passivo_nao_circulante": "REAL",
                "passivos_totais": "REAL",
                "patrimonio_liquido": "REAL",
                "capitalizacao_total": "REAL",
                "ativos_tangiveis": "REAL",
                "capital_de_giro": "REAL",
                "capital_investido": "REAL",
                "valor_contabil": "REAL",
                "divida_total": "REAL",
                "numero_acoes_ordinarias": "REAL",
                "numero_acoes_em_tesouraria": "REAL",
                "PRIMARY KEY": "(perfil_id, ano)",
                "FOREIGN KEY": "(perfil_id) REFERENCES perfil(id) ON DELETE CASCADE",
            },
            "fc": {
                "perfil_id": "INTEGER",
                "ano": "INTEGER NOT NULL",
                "lucro_liquido": "REAL",
                "depreciacao_e_amortizacao": "REAL",
                "variacao_capital_de_giro": "REAL",
                "fluxo_caixa_operacional": "REAL",
                "fluxo_caixa_investimentos": "REAL",
                "dividendos_pagos": "REAL",
                "fluxo_caixa_financiamento": "REAL",
                "variaca_do_caixa": "REAL",
                "posicao_inicial_caixa": "REAL",
                "posicao_final_caixa": "REAL",
                "emissao_acoes": "REAL",
                "emissao_dividas": "REAL",
                "pagamento_dividas": "REAL",
                "compra_acoes": "REAL",
                "fluxo_caixa_livre": "REAL",
                "PRIMARY KEY": "(perfil_id, ano)",
                "FOREIGN KEY": "(perfil_id) REFERENCES perfil(id) ON DELETE CASCADE",
            },
            "stats": {
                "perfil_id": "INTEGER",
                "ano": "INTEGER NOT NULL",
                "roe": "REAL",
                "payout": "REAL",
                "dividendos": "REAL",
                "eps": "REAL",
                "PRIMARY KEY": "(perfil_id, ano)",
                "FOREIGN KEY": "(perfil_id) REFERENCES perfil(id) ON DELETE CASCADE",
            },
        }
        for nome, colunas in tabelas.items():
            self.criar_tabela(nome, colunas)


if __name__ == "__main__":
    with ConexaoBD() as bd:
        gerenciador = GerenciadorBD(bd)
        gerenciador.tabelas_iniciais()

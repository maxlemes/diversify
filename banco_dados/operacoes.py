import logging
import sqlite3

import pandas as pd

import diversify.config_log
from banco_dados.gerenciador import GerenciadorBanco


class OperacoesBanco:
    def __init__(self, gerenciador: GerenciadorBanco):
        """Recebe a instância de GerenciadorBanco e usa sua conexão."""
        self.gerenciador = gerenciador

    def _executar_consulta(self, consulta, parametros=()):
        """Função auxiliar para executar consultas e tratar erros de forma centralizada."""
        try:
            cursor = self.gerenciador.conexao.cursor()
            cursor.execute(consulta, parametros)
            return cursor
        except sqlite3.Error as erro:
            logging.error(f"Erro ao executar consulta: {erro}")
            print(f"Erro ao executar consulta: {erro}")
            return None

    def _inserir_dados_financeiros(self, tipo_dados, dados_dict):
        """Insere dados financeiros nas tabelas 'dre', 'bp', 'fc', 'stats', 'divs', 'ests'."""

        if tipo_dados not in ["dre", "bp", "fc", "stats", "divs", "ests"]:
            logging.error(f"Tabela '{tipo_dados}' não é válida.")
            print(f"Erro: Tabela '{tipo_dados}' não é válida.")
            return

        ativo = dados_dict["ativo"]
        item = dados_dict["item"]
        chk = dados_dict["chk"]
        anos_dict = dados_dict["anos"]

        # Se precisar adiciona novas colunas de anos
        cursor = self.gerenciador.conexao.cursor()
        self._anos_novos(tipo_dados, anos_dict)

        # Criar colunas dinamicamente com base nos anos fornecidos
        colunas_anos = [f"ano_{ano}" for ano in anos_dict.keys()]
        valores_anos = list(anos_dict.values())

        # Inicializando a lista de colunas e valores
        colunas = ["ativo", "chk", "item"] + colunas_anos
        valores = [ativo, chk, item] + valores_anos

        # Adicionar a coluna de ttm ou atual, dependendo das condições
        if "ttm" in dados_dict and dados_dict["ttm"]:
            colunas.append("ttm")
            valores.append(dados_dict["ttm"])

        if "atual" in dados_dict and dados_dict["atual"]:
            colunas.append("atual")
            valores.append(dados_dict["atual"])

        # Criar placeholders dinamicamente
        placeholders = ", ".join(["?" for _ in valores])
        colunas_sql = ", ".join(colunas)

        try:
            consulta = f"""
                INSERT INTO {tipo_dados} ({colunas_sql}) VALUES ({placeholders})
                ON CONFLICT(ativo, chk) DO NOTHING;
            """
            cursor = self._executar_consulta(consulta, valores)
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(
                    f"Dados inseridos na Tabela '{tipo_dados}' para o ativo '{ativo}'."
                )
        except sqlite3.Error as erro:
            logging.error(f"Erro ao inserir dados financeiros: {erro}")
            print(f"Erro ao inserir dados financeiros: {erro}")

    def _anos_novos(self, tipo_dados, anos_dict):
        """
        Função que verifica se há anos novos para serem adicionados à tabela e, caso necessário,
        adiciona novas colunas para os anos ausentes e retorna os anos novos

        Parâmetros:
        cursor: objeto cursor do banco de dados.
        tipo_dados: nome da tabela que contém as colunas dos anos.
        anos_dict: dicionário com os anos que devem estar na tabela.
        """
        # Passo 2: Consultar os anos já presentes na tabela
        cursor = self.gerenciador.conexao.cursor()
        cursor.execute(f"PRAGMA table_info({tipo_dados});")
        colunas = cursor.fetchall()
        colunas_anos = [coluna[1] for coluna in colunas if coluna[1].startswith("ano_")]

        # Passo 3: Verificar se há anos novos para serem adicionados
        anos_novos = [
            ano for ano in anos_dict.keys() if f"ano_{ano}" not in colunas_anos
        ]

        if anos_novos:
            # Passo 4: Adicionar novas colunas para os anos que ainda não existem
            for ano in anos_novos:
                cursor.execute(
                    f"""
                    ALTER TABLE {tipo_dados}
                    ADD COLUMN ano_{ano} REAL;
                """
                )
            return anos_novos
            logging.info(f"Novas colunas de anos adicionadas: {', '.join(anos_novos)}.")
        else:
            logging.info("Não há novos anos para adicionar.")
            return []

    def inserir_perfil(self, nome, ticker, setor, subsetor, descricao):
        """Insere ou atualiza o perfil de um ativo na tabela 'perfil'."""

        try:
            # Inserção ou substituição (caso o ticker já exista)
            consulta = """
                INSERT OR REPLACE INTO perfil (nome, ticker, setor, subsetor, descricao)
                VALUES (?, ?, ?, ?, ?);
            """
            cursor = self._executar_consulta(
                consulta, (nome, ticker, setor, subsetor, descricao)
            )

            # Se a consulta foi executada com sucesso
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(
                    f"Perfil do ativo '{ticker}' inserido ou atualizado com sucesso."
                )
                print(f"Perfil do ativo '{ticker}' inserido ou atualizado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao inserir perfil: {e}")
            print(f"Erro ao  inserir perfil: {e}")

    def inserir_financas(self, tipo_dados, dados_dict):
        """Insere dados financeiros nas tabelas 'dre', 'bp', 'fc', 'stats', 'divs', 'ests'."""

        if tipo_dados not in ["dre", "bp", "fc", "stats", "divs", "ests"]:
            logging.error(f"Tabela '{tipo_dados}' não é válida.")
            print(f"Erro: Tabela '{tipo_dados}' não é válida.")
            return

        ativo = dados_dict["ativo"]
        item = dados_dict["item"]
        chk = dados_dict["chk"]
        anos_dict = dados_dict["anos"]

        try:
            cursor = self.gerenciador.conexao.cursor()

            # Passo 1: Verificar se existe um registro combinando ativo e item
            cursor.execute(
                f"""
                SELECT * FROM {tipo_dados}
                WHERE ativo = ? AND item = ?;
            """,
                (ativo, item),
            )
            resultado = cursor.fetchone()

            if resultado:
                logging.info(
                    f"Registro encontrado para o ativo '{ativo}' e item '{item}'."
                )

                # Se precisar adiciona novas colunas de anos
                anos_novos = self._anos_novos(tipo_dados, anos_dict)

                # # Passo 2: Consultar os anos já presentes na tabela
                # cursor.execute(f"PRAGMA table_info({tipo_dados});")
                # colunas = cursor.fetchall()
                # colunas_anos = [coluna[1] for coluna in colunas if coluna[1].startswith("ano_")]

                # # Passo 3: Verificar se há anos novos para serem adicionados
                # anos_novos = [ano for ano in anos_dict.keys() if f"ano_{ano}" not in colunas_anos]

                # if anos_novos:
                #     # Passo 4: Adicionar novas colunas para os anos que ainda não existem
                #     for ano in anos_novos:
                #         cursor.execute(f'''
                #             ALTER TABLE {tipo_dados}
                #             ADD COLUMN ano_{ano} REAL;
                #         ''')
                #     logging.info(f"Novas colunas de anos adicionadas: {', '.join(anos_novos)}.")

                # Passo 5: Atualizar os dados nas novas colunas (sem apagar as antigas)
                for ano, valor in anos_dict.items():
                    valor = (
                        valor if valor is not None else None
                    )  # Garantir que None seja passado como NULL
                    if ano in anos_novos:
                        cursor.execute(
                            f"""
                            UPDATE {tipo_dados}
                            SET ano_{ano} = ?
                            WHERE ativo = ? AND item = ?;
                        """,
                            (valor, ativo, item),
                        )

                # Passo 6: Atualizar as colunas ttm (caso exista)
                if "ttm" in dados_dict and dados_dict["ttm"]:
                    ttm = dados_dict["ttm"]
                    ttm = (
                        ttm if ttm is not None else None
                    )  # Garantir que None seja passado como NULL
                    cursor.execute(
                        f"""
                        UPDATE {tipo_dados}
                        SET ttm = ?, chk = ?
                        WHERE ativo = ? AND item = ?;
                    """,
                        (ttm, chk, ativo, item),
                    )

                # Passo 7: Atualizar as colunas atual (caso exista)
                if "atual" in dados_dict and dados_dict["atual"]:
                    atual = dados_dict["atual"]
                    atual = (
                        atual if atual is not None else None
                    )  # Garantir que None seja passado como NULL
                    cursor.execute(
                        f"""
                        UPDATE {tipo_dados}
                        SET atual = ?, chk = ?
                        WHERE ativo = ? AND item = ?;
                    """,
                        (atual, chk, ativo, item),
                    )

                self.gerenciador.conexao.commit()
                logging.info(
                    f"Dados atualizados na tabela '{tipo_dados}' para o ativo '{ativo}'."
                )
            else:
                logging.info(
                    f"Registro não encontrado para o ativo '{ativo}' e item '{item}', realizando inserção."
                )
                self._inserir_dados_financeiros(tipo_dados, dados_dict)

        except sqlite3.Error as erro:
            logging.error(f"Erro ao atualizar dados financeiros: {erro}")
            print(f"Erro ao atualizar dados financeiros: {erro}")

    def inserir_dataframe(self, tipo_dados, df):
        """Processa o DataFrame e insere os dados no banco de dados."""

        try:

            # alterando ests_r para ests
            if tipo_dados == "ests_r":
                tipo_dados = "ests"

            ativo = df["ativo"][0]

            for index, row in df.iterrows():
                dados_dict = {
                    "ativo": row["ativo"],
                    "item": row["item"],
                    "chk": row["chk"],
                    "anos": {int(ano): row[ano] for ano in df.columns if ano.isdigit()},
                }

                if "ttm" in row and row["ttm"]:
                    dados_dict["ttm"] = row["ttm"]

                if "atual" in row and row["atual"]:
                    dados_dict["atual"] = row["atual"]

                # Chamando a função para inserir no banco
                self.inserir_financas(tipo_dados, dados_dict)

            logging.info(
                f"Dataframe com dados do ativo {ativo} inseridos com sucesso na tabela {tipo_dados}."
            )
            print(
                f"Dataframe com dados do ativo {ativo} inseridos com sucesso na tabela {tipo_dados}."
            )

        except Exception as e:
            logging.error(
                f"Erro ao inserir dataframe com dados do ativo {ativo} na tabela {tipo_dados}: {e}"
            )
            print(
                f"Erro ao inserir dataframe com dados do ativo {ativo} na tabela {tipo_dados}: {e}"
            )

    def inserir_resumo(
        self,
        ativo,
        cotacao,
        trimestre,
        indicadores,
        dividendos,
        estimativas,
        receita,
    ):
        """Insere ou atualiza o resumo de um ativo na tabela 'resumo'."""

        try:
            # Inserção ou substituição
            consulta = """
                INSERT OR REPLACE INTO resumo (ativo, cotacao, trimestre, indicadores, dividendos, estimativas, receita)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """
            cursor = self._executar_consulta(
                consulta,
                (
                    ativo,
                    cotacao,
                    trimestre,
                    indicadores,
                    dividendos,
                    estimativas,
                    receita,
                ),
            )

            # Se a consulta foi executada com sucesso
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(
                    f"Resumo do ativo '{ativo}' inserido ou atualizado com sucesso."
                )
                print(f"Resumo do ativo '{ativo}' inserido ou atualizado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao inserir resumo no banco de dados: {e}")
            print(f"Erro ao ao inserir resumo no banco de dados: {e}")

    def inserir_precos(self, dados):
        """Insere ou atualiza os preços de um ativo na tabela 'precos'."""

        try:
            # Inserção ou substituição (caso o ativo já exista)
            consulta = """
                INSERT OR IGNORE INTO precos (ativo, data, open, high, low, close, adj_close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """

            # cursor = self._executar_consulta(consulta, dados) # Passa a lista de dados como argumento
            cursor = self.gerenciador.conexao.cursor()
            cursor.executemany(consulta, dados)

            # Se a consulta foi executada com sucesso
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(
                    f"{len(dados)} preços '{dados[0][0]}' inseridos ou atualizados com sucesso."
                )
                print(
                    f"{len(dados)} preços do ativo '{dados[0][0]}' inseridos ou atualizados com sucesso."
                )
        except Exception as e:
            logging.error(f"Erro ao inserir os preços no banco de dados: {e}")
            print(f"Erro ao ao inserir os preços no banco de dados: {e}")

    def consultar_perfil(self, ativo):
        """Consulta um perfil com base no ticker."""
        try:
            consulta = "SELECT * FROM perfil WHERE ticker = ?;"
            cursor = self._executar_consulta(consulta, (ativo,))
            if cursor:
                perfil = cursor.fetchone()
                if perfil:
                    return {
                        "id": perfil[0],
                        "nome": perfil[1],
                        "ticker": perfil[2],
                        "setor": perfil[3],
                        "subsetor": perfil[4],
                        "descricao": perfil[5],
                    }
                else:
                    logging.warning(f"Perfil com ticker '{ativo}' não encontrado.")
                    print(f"Perfil com ticker '{ativo}' não encontrado.")
                    return None
        except sqlite3.Error as erro:
            logging.error(f"Erro ao consultar o perfil: {erro}")
            print(f"Erro ao consultar o perfil: {erro}")
            return None

    def consultar_financas(self, tipo_dados, ativo=None, termo=None):
        """Consulta dados financeiros filtrando por ativo, tabela e descrição do item com base em um termo fornecido."""

        # alterando ests_r para ests
        if tipo_dados == "ests_r":
            tipo_dados = "ests"

        if tipo_dados not in ["dre", "bp", "fc", "stats", "divs", "ests"]:
            logging.error(f"Tabela '{tipo_dados}' não é válida.")
            print(f"Erro: Tabela '{tipo_dados}' não é válida.")
            return

        # Construir a consulta de forma dinâmica, dependendo de quais parâmetros foram passados
        consulta = f"SELECT * FROM {tipo_dados} WHERE 1=1 "
        parametros = []

        # Se um ativo for fornecido, adicionar o filtro para o ativo
        if ativo:
            consulta += "AND LOWER(ativo) = LOWER(?) "
            parametros.append(ativo.lower())

        # Se um termo for fornecido, adicionar o filtro para o item (com LIKE)
        if termo:
            consulta += "AND LOWER(item) LIKE LOWER(?) "
            parametros.append(f"%{termo.lower()}%")

        consulta += "ORDER BY ativo;"

        try:
            # Executar a consulta
            cursor = self._executar_consulta(consulta, tuple(parametros))

            if cursor:
                resultados = cursor.fetchall()
                if resultados:
                    logging.info(
                        f"Resultados encontrados para {'ativo' if ativo else ''} "
                        f"{ativo if ativo else ''} na tabela '{tipo_dados}':"
                    )
                    return [
                        list(resultado) for resultado in resultados
                    ]  # Retorna os resultados em formato de lista
                else:
                    logging.info(
                        f"Nenhum resultado encontrado para o ativo '{ativo}' na tabela '{tipo_dados}'."
                    )
                    print(
                        f"Nenhum resultado encontrado para o ativo '{ativo}' na tabela '{tipo_dados}'."
                    )

        except sqlite3.Error as erro:
            logging.error(f"Erro ao consultar dados financeiros: {erro}")
            print(f"Erro ao consultar dados financeiros: {erro}")
            return []

    def consultar_resumo(self, ativo):
        """Consulta o resumo dos dados do ativo."""
        try:
            consulta = "SELECT * FROM resumo WHERE ativo = ?;"
            cursor = self._executar_consulta(consulta, (ativo,))
            if cursor:
                perfil = cursor.fetchone()
                if perfil:
                    return {
                        "id": perfil[0],
                        "ativo": perfil[1],
                        "cotacao": perfil[2],
                        "trimestre": perfil[3],
                        "indicadores": perfil[4],
                        "dividendos": perfil[5],
                        "estimativas": perfil[6],
                        "receita": perfil[7],
                    }
                else:
                    logging.warning(f"Resumo com '{ativo}' não encontrado.")
                    print(f"Resumo com '{ativo}' não encontrado.")
                    return None
        except sqlite3.Error as erro:
            logging.error(f"Erro ao consultar resumo: {erro}")
            print(f"Erro ao consultar resumo: {erro}")
            return None

    def consultar_precos(self, ativo, colunas=None):
        """Consulta informações específicas sobre um ativo no banco de dados.

        Parâmetros:
            ativo (str): O nome do ativo a ser consultado.
            colunas (list, opcional): Lista de colunas a serem retornadas.
                                    Se None, retorna todas as colunas.

        Retorna:
            dict: Um dicionário com os dados consultados ou None se não encontrar.
        """
        try:
            # Se nenhuma coluna for especificada, retorna todas
            if not colunas:
                colunas = [
                    "ativo",
                    "data",
                    "open",
                    "high",
                    "low",
                    "close",
                    "adj_close",
                    "volume",
                ]

            # Monta a query dinamicamente com as colunas desejadas
            colunas_sql = ", ".join(colunas)
            consulta = f"SELECT {colunas_sql} FROM precos WHERE ativo = ?;"

            # Executa a consulta
            cursor = self._executar_consulta(consulta, (ativo,))
            if cursor:
                resultado = cursor.fetchall()
                if resultado:
                    return [
                        dict(zip(colunas, linha)) for linha in resultado
                    ]  # Converte para dicionário
                else:
                    logging.warning(f"Dados do ativo '{ativo}' não encontrados.")
                    print(f"Dados do ativo '{ativo}' não encontrados.")
                    return None
        except sqlite3.Error as erro:
            logging.error(f"Erro ao consultar preços: {erro}")
            print(f"Erro ao consultar preços: {erro}")
            return None

    def remover_financas(self, tipo_dados, ativo, item, chk):
        """Remove um registro financeiro de uma tabela específica com base no ativo, item e chk."""

        # alterando ests_r para ests
        if tipo_dados == "ests_r":
            tipo_dados = "ests"

        if tipo_dados not in ["dre", "bp", "fc", "stats", "divs", "ests"]:
            logging.error(f"Tabela '{tipo_dados}' não é válida.")
            print(f"Erro: Tabela '{tipo_dados}' não é válida.")
            return

        try:
            # Executar a remoção
            consulta = f"""
                DELETE FROM {tipo_dados}
                WHERE ativo = ? AND item = ? AND chk = ?;
            """
            cursor = self._executar_consulta(consulta, (ativo, item, chk))
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(
                    f"Registro removido da tabela '{tipo_dados}' para o ativo '{ativo}', item '{item}'."
                )
                print(
                    f"Registro removido da tabela '{tipo_dados}' para o ativo '{ativo}', item '{item}'."
                )
        except sqlite3.Error as erro:
            logging.error(f"Erro ao remover dados financeiros: {erro}")
            print(f"Erro ao remover dados financeiros: {erro}")

    def listar_colunas(self, tipo_dados):
        """Retorna os nomes das colunas de uma tabela no SQLite."""

        # alterando ests_r para ests
        if tipo_dados == "ests_r":
            tipo_dados = "ests"

        consulta = f"PRAGMA table_info({tipo_dados});"
        cursor = self._executar_consulta(consulta)

        if cursor:
            return [
                linha[1] for linha in cursor.fetchall()
            ]  # O nome da coluna está no índice 1
        return []

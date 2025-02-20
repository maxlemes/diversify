import logging
import os
import sqlite3


class GerenciadorBanco:
    def __init__(
        self, caminho_banco="dados/banco_de_dados.db"
    ):  # observe o endereço e nome do banco de dados
        """Inicializa a conexão com o banco de dados."""
        os.makedirs(os.path.dirname(caminho_banco), exist_ok=True)
        self.caminho_banco = caminho_banco
        self.conexao = None
        self.criar_conexao()

    def criar_conexao(self):
        """Cria e retorna a conexão com o banco de dados."""
        try:
            self.conexao = sqlite3.connect(
                self.caminho_banco
            )  # Armazena a conexão em self.conexao
            logging.info(
                f"Conexão com o banco '{self.caminho_banco}' estabelecida com sucesso."
            )
        except sqlite3.Error as erro:
            logging.error(f"Erro ao conectar com o banco de dados: {erro}")
            print(f"Erro ao conectar com o banco de dados: {erro}")

    def criar_tabelas(self):
        """Cria as tabelas no banco de dados, se não existirem."""
        try:
            cursor = self.conexao.cursor()

            # Tabela 'perfil'
            comando_perfil = """
            CREATE TABLE IF NOT EXISTS perfil (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                ticker TEXT NOT NULL,
                setor TEXT,
                subsetor TEXT,
                descricao TEXT,
                UNIQUE (ticker)
            );
            """
            cursor.execute(comando_perfil)

            # Tabelas 'dre', 'fc'
            tabelas = ["dre", "fc"]
            for tabela in tabelas:
                comando_tabela = f"""
                CREATE TABLE IF NOT EXISTS {tabela} (
                    id INTEGER PRIMARY KEY,
                    ativo TEXT NOT NULL,
                    item TEXT NOT NULL,
                    chk REAL,
                    ttm REAL,
                    ano_2019 REAL,
                    ano_2020 REAL,
                    ano_2021 REAL,
                    ano_2022 REAL,
                    ano_2023 REAL,
                    UNIQUE (ativo, chk)
                );
                """
                cursor.execute(comando_tabela)

            # Tabelas 'bp', 'divs'
            tabelas = ["bp", "divs"]
            for tabela in tabelas:
                comando_tabela = f"""
                CREATE TABLE IF NOT EXISTS {tabela} (
                    id INTEGER PRIMARY KEY,
                    ativo TEXT NOT NULL,
                    item TEXT NOT NULL,
                    chk REAL,
                    ano_2019 REAL,
                    ano_2020 REAL,
                    ano_2021 REAL,
                    ano_2022 REAL,
                    ano_2023 REAL,
                    UNIQUE (ativo, chk)
                );
                """
                cursor.execute(comando_tabela)

            # Tabela stats
            comando_tabela = f"""
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY,
                    ativo TEXT NOT NULL,
                    item TEXT NOT NULL,
                    chk REAL,
                    atual REAL,
                    ano_2019 REAL,
                    ano_2020 REAL,
                    ano_2021 REAL,
                    ano_2022 REAL,
                    ano_2023 REAL,
                    UNIQUE (ativo, chk)
                );
                """
            cursor.execute(comando_tabela)

            # Tabela ests
            comando_tabela = f"""
                CREATE TABLE IF NOT EXISTS ests (
                    id INTEGER PRIMARY KEY,
                    ativo TEXT NOT NULL,
                    item TEXT NOT NULL,
                    chk REAL,
                    ttm REAL,
                    ano_2019 REAL,
                    ano_2020 REAL,
                    ano_2021 REAL,
                    ano_2022 REAL,
                    ano_2023 REAL,
                    ano_2024 REAL,
                    ano_2025 REAL,
                    ano_2026 REAL,
                    UNIQUE (ativo, chk)
                );
                """
            cursor.execute(comando_tabela)

            # Tabela resumo
            comando_tabela = f"""
                CREATE TABLE IF NOT EXISTS resumo (
                    id INTEGER,
                    ativo TEXT NOT NULL,
                    cotacao REAL,
                    trimestre TEXT,
                    indicadores TEXT,
                    dividendos TEXT,
                    estimativas TEXT,
                    receita TEXT,
                    PRIMARY KEY (ativo, id)
                );
                """
            cursor.execute(comando_tabela)

            # Tabela precos
            comando_tabela = f"""
                CREATE TABLE IF NOT EXISTS precos (
                    ativo TEXT NOT NULL,
                    data TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    adj_close REAL,
                    volume INTEGER,
                    PRIMARY KEY (ativo, data)
                );
                """
            cursor.execute(comando_tabela)

            self.conexao.commit()
            logging.info("Tabelas criadas ou já existentes com sucesso.")
            print("Tabelas criadas ou já existentes com sucesso.")
        except sqlite3.Error as erro:
            logging.error(f"Erro ao criar as tabelas: {erro}")
            print(f"Erro ao criar as tabelas: {erro}")

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        try:
            if self.conexao:
                self.conexao.close()
                logging.info(
                    f"Conexão com o banco '{self.caminho_banco}' fechada com sucesso."
                )
                print(
                    f"Conexão com o banco '{self.caminho_banco}' fechada com sucesso."
                )
        except sqlite3.Error as erro:
            logging.error(f"Erro ao fechar a conexão com o banco de dados: {erro}")
            print(f"Erro ao fechar a conexão com o banco de dados: {erro}")


# Exemplo de uso roda se o arquivo for executado diretamente (python gerenciador.py).
if __name__ == "__main__":
    banco = GerenciadorBanco()  # Cria uma instância da classe e conecta ao banco
    banco.criar_tabelas()  # Chama o método criar_tabelas() que cria as tabelas
    banco.fechar_conexao()  # Fecha a conexão corretamente

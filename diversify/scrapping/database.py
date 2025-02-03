# Esse arquivo será responsável por:
# Criar e gerenciar o banco de dados.
# Salvar os dados extraídos pelo scraper.py.

import os
import re
import sqlite3
import pandas as pd

# Caminho absoluto para dados.db na raiz do projeto
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))
)  # Sobe três níveis
DB_NAME = os.path.join(BASE_DIR, 'dados.db')


def conectar():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    """Cria as tabelas no banco de dados (se não existirem)."""
    conn = conectar()
    cursor = conn.cursor()

    # Criando a tabela 'ativos'
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ativos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            website TEXT,
            cotacao TEXT
        )
    """
    )

    # Criando a tabela 'valores_ativos'
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS valores_ativos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,  -- Código do ativo (ex: WEGE3)
            ano TEXT NOT NULL,   -- Ano do valor do indicador
            indicador TEXT NOT NULL,  -- Nome do indicador (ex: "P/L", "ROE", "Dívida/Patrimônio")
            valor TEXT NOT NULL,  -- Valor do indicador correspondente
            UNIQUE(ticker, ano, indicador),
            FOREIGN KEY (ticker) REFERENCES ativos (ticker)
        )
    """
    )

    # Commit para garantir que as alterações sejam salvas no banco de dados
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()


def salvar_profile(dados):
    """Salva os dados perfil do ativo na tabela ativos."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ativos (ticker, nome, descricao, website, cotacao)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(ticker) DO UPDATE SET
            nome = excluded.nome,
            descricao = excluded.descricao,
            website = excluded.website, 
            cotacao = excluded.cotacao
    """,
        (
            dados['ticker'],
            dados['nome'],
            dados['descricao'],
            dados['website'],
            dados['cotacao'],
        ),
    )

    conn.commit()
    conn.close()


def salvar_indicadores(dados):
    """Salva os EPS do ativo na tabela valores_ativos."""
    conn = conectar()
    cursor = conn.cursor()

    try:
        # Iterando sobre a lista de dicionários e inserindo no banco
        for dado in dados:
            if bool(re.match(r"^-?\d+(\.\d+)?$", str(dado['valor']))):

                if dado['ano'] == 'Atual':
                    dado['ano'] = 'TTM'

                # Se o ano for "TTM", sempre insere sem verificar duplicação
                if dado['ano'] in ['TTM']:
                    cursor.execute(
                        """
                        INSERT INTO valores_ativos (ticker, ano, indicador, valor)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(ticker, ano, indicador) DO UPDATE
                        SET valor = excluded.valor
                        """,
                        (dado['ticker'], dado['ano'], dado['indicador'], dado['valor']),
                    )
                else:
                    # Verificar se o ativo, ano e indicador já existem na tabela
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM valores_ativos
                        WHERE ticker = ? AND ano = ? AND indicador = ?
                        """,
                        (dado['ticker'], dado['ano'], dado['indicador']),
                    )

                    resultado = cursor.fetchone()

                    if resultado[0] == 0:
                        cursor.execute(
                            """
                            INSERT INTO valores_ativos (ticker, ano, indicador, valor)
                            VALUES (?, ?, ?, ?)
                            """,
                            (dado['ticker'], dado['ano'], dado['indicador'], dado['valor']),
                        )
                    else:
                        print(f"Registro duplicado: {dado['ticker']} - {dado['ano']} - {dado['indicador']}")

        conn.commit()  # Commit após todas as inserções

    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
    finally:
        conn.close()


def consultar_ativos(tabela):
    """Consulta e retorna todos os ativos salvos no banco."""
    conn = conectar()
    query = f'SELECT * FROM {tabela}'  # Interpolação de strings para inserir o nome da tabela
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

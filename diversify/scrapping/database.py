# Esse arquivo será responsável por:
# Criar e gerenciar o banco de dados.
# Salvar os dados extraídos pelo scraper.py.

import os
import sqlite3
import pandas as pd

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "dados.db")

def conectar():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    """Cria a tabela ativos no banco de dados (se não existir)."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ativos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            website TEXT
        )
    """)

    conn.commit()
    conn.close()

def salvar_ativo(dados):
    """Salva os dados do ativo na tabela ativos."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ativos (ticker, nome, descricao, website)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(ticker) DO UPDATE SET
            nome = excluded.nome,
            descricao = excluded.descricao,
            website = excluded.website
    """, (dados["ticker"], dados["nome"], dados["descricao"], dados["website"]))

    conn.commit()
    conn.close()

def consultar_ativos():
    """Consulta e retorna todos os ativos salvos no banco."""
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM ativos", conn)
    conn.close()
    return df


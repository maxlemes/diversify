
import re

def consultar_dados(self, ativo=None, tipo_balanco='dre', entrada=None):
    """
    Consulta os dados no banco de dados com filtros opcionais.

    Parâmetros:
        ativo (str, opcional): Código do ativo a buscar.
        ano (int, opcional): Ano para buscar a coluna correspondente (ano_YYYY).
        tipo_balanco (str, opcional): Nome da tabela no banco (padrão: 'dre').
        entrada (str, opcional): Busca um termo específico em uma coluna específica.

    Retorna:
        list: Lista de tuplas contendo os resultados da consulta.
    """
    
    # Valida o nome da tabela para evitar SQL Injection
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tipo_balanco):
        raise ValueError(f"Nome de tabela inválido: {tipo_balanco}")

    # Verifica se a tabela existe antes de executar a consulta
    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tipo_balanco,))
    if not self.cursor.fetchone():
        raise ValueError(f"Tabela '{tipo_balanco}' não encontrada no banco de dados.")

    query = f"SELECT * FROM {tipo_balanco} WHERE 1=1"
    params = []

    if ativo:
        query += " AND ativo = ?"
        params.append(ativo)

    if entrada:
        # Busca na coluna 'descricao' (ou outra relevante) ao invés de todas as colunas
        query += " AND UPPER(tipo) LIKE UPPER(?)"
        params.append(f"%{entrada}%")

    self.cursor.execute(query, params)
    return self.cursor.fetchall()

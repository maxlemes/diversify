import sqlite3

def salvar_tabela(self, ativo, tipo_balanco, df):
    """Salva ou atualiza o perfil do ativo no banco de dados, evitando duplicação de linhas."""
    
    # Adiciona a coluna 'ativo' ao DataFrame
    df.insert(0, 'ativo', [ativo] * len(df))

    # Renomeia colunas (anos, TTM e outras)
    novas_colunas = {"Moeda: BRL": 'tipo'}
    novas_colunas.update({col: f"ano_{col}" for col in df.columns if str(col).isdigit()})
    novas_colunas["TTM"] = "ttm"
    df = df.rename(columns=lambda col: novas_colunas.get(col, col))

    print(df)

    # Obtém as colunas existentes na tabela
    self.cursor.execute(f"PRAGMA table_info('{tipo_balanco}')")
    colunas_existentes = {row[1] for row in self.cursor.fetchall()}

    # Criar tabela se não existir
    if not colunas_existentes:
        colunas_sql = [f"{col} REAL" if col.startswith("ano_") or col == "ttm" or col == "chk" else f"{col} TEXT" for col in df.columns]
        query = f"CREATE TABLE {tipo_balanco} ({', '.join(colunas_sql)}, PRIMARY KEY (ativo, chk))"

        print("Query gerada:", query)  # <-- Adicione esta linha para depuração

        self.cursor.execute(query)
        colunas_existentes = set(df.columns)

    else:
        # Adicionar colunas novas na tabela
        for col in df.columns:
            if col not in colunas_existentes:
                tipo = "REAL" if col.startswith("ano_") or col == "ttm" or col == "chk"  else "TEXT"
                self.cursor.execute(f"ALTER TABLE {tipo_balanco} ADD COLUMN {col} {tipo}")
                colunas_existentes.add(col)

    # Filtra apenas as colunas que existem na tabela
    df = df[list(colunas_existentes)]

    # Gerar query dinâmica usando INSERT OR REPLACE para evitar duplicação
    colunas = df.columns.tolist()
    placeholders = ", ".join(["?"] * len(colunas))
    query_insert = f"""
        INSERT OR REPLACE INTO {tipo_balanco} ({', '.join(colunas)}) 
        VALUES ({placeholders})
    """

    # Inserir os dados no banco
    self.cursor.executemany(query_insert, df.to_numpy().tolist())

    # Commit para salvar as alterações
    self.conn.commit()

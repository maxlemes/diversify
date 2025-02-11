def criar_tabelas(self, nome_tabela, colunas):
        """Cria ou atualiza a tabela 'nome_tabela' no banco de dados."""
        
        # Obtém as colunas existentes na tabela
        self.cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas_existentes = {row[1] for row in self.cursor.fetchall()}  # Nome das colunas existentes

        colunas_sql = []
        novas_colunas = []

        for col in colunas:
            col_formatado = f"ano_{col}" if col.isdigit() else col.lower()

            # Adiciona apenas colunas novas
            if col_formatado not in colunas_existentes:
                novas_colunas.append(col_formatado)

            tipo = "REAL" if col.isdigit() or col.lower() == "ttm" else "TEXT"
            colunas_sql.append(f"{col_formatado} {tipo}")

        # Criar tabela se não existir
        if not colunas_existentes:
            query = f'''
                CREATE TABLE {nome_tabela} (
                    {', '.join(colunas_sql)}
                )
            '''
            self.cursor.execute(query)
        else:
            # Adicionar colunas novas se necessário
            for col in novas_colunas:
                tipo = "REAL" if col.startswith("ano_") or col == "ttm" else "TEXT"
                self.cursor.execute(f"ALTER TABLE {nome_tabela} ADD COLUMN {col} {tipo}")

        self.conn.commit()
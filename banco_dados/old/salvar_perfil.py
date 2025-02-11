def salvar_perfil(self, ativo):
        """Salva ou atualiza o perfil do ativo no banco de dados se houver diferenças."""
        
        # Verifica se o ativo já está no banco de dados
        self.cursor.execute('''
            SELECT nome, ticker, setor, subsetor, descricao 
            FROM perfil 
            WHERE ticker = ?
        ''', (ativo.ticker,))
        
        resultado = self.cursor.fetchone()

        # Se o ativo já existir e os dados forem diferentes, atualiza
        if resultado:
            if resultado != (ativo.nome, ativo.ticker, ativo.setor, ativo.subsetor, ativo.descricao):
                self.cursor.execute('''
                    UPDATE perfil 
                    SET nome = ?, setor = ?, subsetor = ?, descricao = ?
                    WHERE ticker = ?
                ''', (ativo.nome, ativo.setor, ativo.subsetor, ativo.descricao, ativo.ticker))
                self.conn.commit()
        else:
            # Caso contrário, insere um novo registro
            self.cursor.execute('''
                INSERT INTO perfil (nome, ticker, setor, subsetor, descricao)
                VALUES (?, ?, ?, ?, ?)
            ''', (ativo.nome, ativo.ticker, ativo.setor, ativo.subsetor, ativo.descricao))
            self.conn.commit()
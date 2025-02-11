import sqlite3
import logging

from banco_dados.gerenciador import GerenciadorBanco

# Configuração do log
logging.basicConfig(
    filename="operacoes_banco.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

    def inserir_perfil(self, nome, ticker, setor, subsetor, descricao):
        """Insere um ativo na tabela 'perfil'."""
        try:
            consulta = '''
                INSERT INTO perfil (nome, ticker, setor, subsetor, descricao)
                VALUES (?, ?, ?, ?, ?);
            '''
            cursor = self._executar_consulta(consulta, (nome, ticker, setor, subsetor, descricao))
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(f"Perfil do ativo '{ticker}' inserido com sucesso.")
                print(f"Perfil do ativo '{ticker}' inserido com sucesso.")
        except sqlite3.IntegrityError:
            logging.warning(f"O ativo '{ticker}' já existe no banco de dados.")
            print(f"Erro: O ativo '{ticker}' já existe no banco de dados.")

    def _inserir_dados_financeiros(self, tabela, ativo, item, chk, ttm, anos_valores):
        """Insere dados financeiros nas tabelas 'dre', 'bp', 'fc', 'stats', 'divs', 'ests'."""
        if tabela not in ['dre', 'bp', 'fc', 'stats', 'divs', 'ests']:
            logging.error(f"Tabela '{tabela}' não é válida.")
            print(f"Erro: Tabela '{tabela}' não é válida.")
            return

        # Validação de dados
        if not isinstance(anos_valores, dict) or not isinstance(ttm, (int, float)) or not isinstance(chk, (int, float)):
            logging.error("Parâmetros inválidos fornecidos para a inserção de finanças.")
            print("Erro: Parâmetros inválidos.")
            return

        # Criar colunas dinamicamente com base nos anos fornecidos
        colunas_anos = [f"ano_{ano}" for ano in anos_valores.keys()]
        valores_anos = list(anos_valores.values())

        # Adicionar colunas fixas (ativo, item, ttm, chk)
        colunas = ["ativo", "chk", "item"] + colunas_anos + ["ttm"]
        valores = [ativo, chk, item] + valores_anos + [ttm]

        # Criar placeholders dinamicamente
        placeholders = ", ".join(["?" for _ in valores])
        colunas_sql = ", ".join(colunas)

        try:
            consulta = f'''
                INSERT INTO {tabela} ({colunas_sql}) VALUES ({placeholders})
                ON CONFLICT(ativo, chk) DO NOTHING;
            '''
            cursor = self._executar_consulta(consulta, valores)
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(f"Dados inseridos na tabela '{tabela}' para o ativo '{ativo}'.")
                print(f"Dados inseridos na tabela '{tabela}' para o ativo '{ativo}'.")
        except sqlite3.Error as erro:
            logging.error(f"Erro ao inserir dados financeiros: {erro}")
            print(f"Erro ao inserir dados financeiros: {erro}")

    def consultar_perfil(self, ticker):
        """Consulta um perfil com base no ticker."""
        try:
            consulta = "SELECT * FROM perfil WHERE ticker = ?;"
            cursor = self._executar_consulta(consulta, (ticker,))
            if cursor:
                perfil = cursor.fetchone()
                if perfil:
                    return {
                        'id': perfil[0],
                        'nome': perfil[1],
                        'ticker': perfil[2],
                        'setor': perfil[3],
                        'subsetor': perfil[4],
                        'descricao': perfil[5]
                    }
                else:
                    logging.warning(f"Perfil com ticker '{ticker}' não encontrado.")
                    print(f"Perfil com ticker '{ticker}' não encontrado.")
                    return None
        except sqlite3.Error as erro:
            logging.error(f"Erro ao consultar o perfil: {erro}")
            print(f"Erro ao consultar o perfil: {erro}")
            return None

    def consultar_financas(self, tabela, ativo, termo):
        """Consulta dados financeiros filtrando por ativo, tabela e descrição do item com base em um termo fornecido."""
        if tabela not in ['dre', 'bp', 'fc', 'stats', 'divs', 'ests']:
            logging.error(f"Tabela '{tabela}' não é válida.")
            print(f"Erro: Tabela '{tabela}' não é válida.")
            return 

        try:
            consulta = f'''
                SELECT * FROM {tabela} 
                WHERE LOWER(ativo) = LOWER(?) AND LOWER(item) LIKE LOWER(?) 
                ORDER BY ativo;
            '''
            cursor = self._executar_consulta(consulta, (ativo.lower(), '%' + termo.lower() + '%'))

            if cursor:
                resultados = cursor.fetchall()
                if resultados:
                    logging.info(f"Resultados encontrados para o ativo '{ativo}' na tabela '{tabela}':")
                    return list(resultados[0]) # # Retorna a lista com os resultados                  
                else:
                    logging.info(f"Nenhum resultado encontrado para o termo '{termo}' no ativo '{ativo}' na tabela '{tabela}'.")
                    print(f"Nenhum resultado encontrado para o termo '{termo}' no ativo '{ativo}' na tabela '{tabela}'.")

        except sqlite3.Error as erro:
            logging.error(f"Erro ao consultar dados financeiros: {erro}")
            print(f"Erro ao consultar dados financeiros: {erro}")
            return []

    def inserir_financas(self, tabela, ativo, item, chk, ttm, anos):
        """Atualiza dados financeiros, adiciona novas colunas de anos, insere dados e atualiza ttm e chk."""
        if tabela not in ['dre', 'bp', 'fc', 'stats', 'divs', 'ests']:
            logging.error(f"Tabela '{tabela}' não é válida.")
            print(f"Erro: Tabela '{tabela}' não é válida.")
            return

        try:
            cursor = self.gerenciador.conexao.cursor()

            # Passo 1: Verificar se existe um registro combinando ativo e item
            cursor.execute(f'''
                SELECT * FROM {tabela}
                WHERE ativo = ? AND item = ?;
            ''', (ativo, item))
            resultado = cursor.fetchone()

            if resultado:
                logging.info(f"Registro encontrado para o ativo '{ativo}' e item '{item}'.")

                # Passo 2: Consultar os anos já presentes na tabela
                cursor.execute(f"PRAGMA table_info({tabela});")
                colunas = cursor.fetchall()
                colunas_anos = [coluna[1] for coluna in colunas if coluna[1].startswith("ano_")]

                # Passo 3: Verificar se há anos novos para serem adicionados
                anos_novos = [ano for ano in anos.keys() if f"ano_{ano}" not in colunas_anos]

                if anos_novos:
                    # Passo 4: Adicionar novas colunas para os anos que ainda não existem
                    for ano in anos_novos:
                        cursor.execute(f'''
                            ALTER TABLE {tabela}
                            ADD COLUMN ano_{ano} REAL;
                        ''')
                    logging.info(f"Novas colunas de anos adicionadas: {', '.join(anos_novos)}.")

                # Passo 5: Atualizar os dados nas novas colunas (sem apagar as antigas)
                for ano, valor in anos.items():
                    if ano in anos_novos:
                        cursor.execute(f'''
                            UPDATE {tabela}
                            SET ano_{ano} = ?
                            WHERE ativo = ? AND item = ?;
                        ''', (valor, ativo, item))

                # Passo 6: Atualizar as colunas ttm
                cursor.execute(f'''
                    UPDATE {tabela}
                    SET ttm = ?, chk = ?
                    WHERE ativo = ? AND item = ?;
                ''', (ttm, chk, ativo, item))

                self.gerenciador.conexao.commit()
                logging.info(f"Dados atualizados na tabela '{tabela}' para o ativo '{ativo}'.")
                print(f"Dados atualizados na tabela '{tabela}' para o ativo '{ativo}'.")
            else:
                logging.info(f"Registro não encontrado para o ativo '{ativo}' e item '{item}', realizando inserção.")
                self._inserir_dados_financeiros(tabela, ativo, item, chk, ttm, anos)

        except sqlite3.Error as erro:
            logging.error(f"Erro ao atualizar dados financeiros: {erro}")
            print(f"Erro ao atualizar dados financeiros: {erro}")

    def remover_financas(self, tabela, ativo, item, chk):
        """Remove um registro financeiro de uma tabela específica com base no ativo, item e chk."""
        if tabela not in ['dre', 'bp', 'fc', 'stats', 'divs', 'ests']:
            logging.error(f"Tabela '{tabela}' não é válida.")
            print(f"Erro: Tabela '{tabela}' não é válida.")
            return

        try:
            # Executar a remoção
            consulta = f'''
                DELETE FROM {tabela}
                WHERE ativo = ? AND item = ? AND chk = ?;
            '''
            cursor = self._executar_consulta(consulta, (ativo, item, chk))
            if cursor:
                self.gerenciador.conexao.commit()
                logging.info(f"Registro removido da tabela '{tabela}' para o ativo '{ativo}', item '{item}'.")
                print(f"Registro removido da tabela '{tabela}' para o ativo '{ativo}', item '{item}'.")
        except sqlite3.Error as erro:
            logging.error(f"Erro ao remover dados financeiros: {erro}")
            print(f"Erro ao remover dados financeiros: {erro}")

    def listar_colunas(self, tabela):
        """Retorna os nomes das colunas de uma tabela no SQLite."""
        consulta = f"PRAGMA table_info({tabela});"
        cursor = self._executar_consulta(consulta)

        if cursor:
            return [linha[1] for linha in cursor.fetchall()]  # O nome da coluna está no índice 1
        return []


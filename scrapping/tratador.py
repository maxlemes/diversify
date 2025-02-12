import pandas as pd
import re

class TratadorDeDados:
    def __init__(self, ativo, dados):
        """Inicializa a classe com os dados coletados."""
        self.ativo = ativo
        self.dados = dados

    def processar_cabecalho(self, linha):
        """
        Processa a primeira linha (cabeçalho) extraída da tabela.
        - Remove os dois primeiros elementos.
        - Divide o segundo item por '\n' e substitui no lugar original.
        - Retorna uma lista contendo o primeiro item e os 6 últimos anos.

        Parâmetros:
            linha (list): Lista contendo os dados da linha da tabela.

        Retorna:
            list: Lista processada.
        """
        linha = linha[2:]  # Remove os dois primeiros elementos
        linha[1:2] = linha[1].split('\n')  # Divide o segundo item por '\n'

        # Seleciona o primeiro item e os 6 últimos valores que estão nas posições ímpares
        linha = [linha[0]] + [item for i, item in enumerate(linha) if i % 2 != 0][-6:]
        
        return linha

    def processar_linha(self, linha):
        """
        Processa uma linha extraída de uma tabela.
        - Remove os dois primeiros elementos.
        - Divide o terceiro item por '\n' e substitui no lugar original.
        - Remove caracteres unicode indesejados.
        - Separa a linha em duas listas: valores e crescimento.
        - Adiciona o prefixo 'Cresc. ' ao primeiro item da lista de crescimento.

        Parâmetros:
            linha (list): Lista contendo os dados da linha da tabela.

        Retorna:
            tuple: (lista de valores, lista de crescimento)
        """
        linha = linha[2:]
        linha[2:3] = linha[2].split('\n')  # Substitui o terceiro item pela lista de duas partes

        # Remove caracteres unicode indesejados
        linha = [re.sub(r'[\u202a\u202c\u202f]', '', item) for item in linha]
        linha = [re.sub('—' , '', item) for item in linha]

        # Condição para listas com 9 ou menos (sem dados de crescimento)
        if len(linha) <= 9:
            linha = linha[:1] + linha[2:-1]  # Eliminar o 2º e o último item
            linha = [linha[0]] + [self.converter_valor(valor) for valor in linha[1:]]
            return linha  # Retorna a linha processada
        else:
            linha_res = [item for i, item in enumerate(linha) if i % 2 == 0]
            linha_res = [linha_res[0]] + [self.converter_valor(valor) for valor in linha_res[1:]]
            
            linha_cres = [item for i, item in enumerate(linha) if i % 2 != 0]
            linha_cres = [linha_cres[0]] + [
                (self.converter_valor(valor) / 100 if self.converter_valor(valor) is not None else None)
                for valor in linha_cres[1:]
                ]
            
            if linha_cres:
                linha_cres[0] = 'Cresc. ' + linha_res[0]
            
            return [linha_res, linha_cres]

    def converter_valor(self, valor):
        """
        Converte valores monetários em strings para números:
        - 'B' (bilhão) → multiplica por 1e9
        - 'M' (milhão) → multiplica por 1e6
        - 'K' (milhar) → multiplica por 1e3

        Parâmetros:
            valor (str): O valor a ser convertido.

        Retorna:
            float: O valor convertido em número.
        """
        if isinstance(valor, str):  # Garante que é uma string
            valor = valor.replace(',', '.')  # Troca vírgula por ponto
            valor = valor.replace('−', '-')  # Fix Unicode minus (U+2212)
            valor = valor.replace('%', '')  # remove os simbolos de % 

            if valor.endswith('B'):
                return float(valor[:-1]) * 1e9
            elif valor.endswith('M'):
                return float(valor[:-1]) * 1e6
            elif valor.endswith('K'):
                return float(valor[:-1]) * 1e3
        return float(valor) if valor else None  # Retorna como está se não for uma string conversível

    def criar_dataframe(self):
        """
        Cria um DataFrame a partir de uma tabela processada.
        A função processa o cabeçalho e as linhas da tabela, tratando casos em que
        cada linha pode ser uma única linha ou uma lista com duas linhas.

        Retorna:
            pd.DataFrame: DataFrame com os dados processados.
        """
        # Processa o cabeçalho
        names = self.processar_cabecalho(self.dados[0])

        # Criar uma lista para armazenar as linhas
        dados = []

        # Processa cada linha da tabela, começando da linha 1
        for i in range(1, len(self.dados)):
            linha = self.dados[i]
            linha_processada = self.processar_linha(linha)

            # Verificar se linha_processada é uma lista com uma ou duas linhas
            if isinstance(linha_processada[0], list):
                dados.extend(linha_processada)  # Se for uma lista de listas, adiciona ambas as linhas
            else:
                dados.append(linha_processada)  # Caso contrário, adiciona apenas uma linha

        # Criar o DataFrame com as linhas processadas
        df = pd.DataFrame(dados, columns=names)

        # Criando a coluna 'check' com o produto das últimas 6 colunas (ignorando NaN)
        df['chk'] = df.iloc[:, -6:].prod(axis=1, skipna=True)

        # Reorganizar as colunas:
        if df.shape[1] > 2:  # Garantir que há pelo menos três colunas
            colunas = df.columns.tolist()
            ultima = colunas[-1]   # Última coluna
            penultima = colunas[-2]  # Penúltima coluna
            
            # Nova ordem: primeira, última, penúltima, e o restante
            nova_ordem = [colunas[0], ultima, penultima] + colunas[1:-2]
            df = df[nova_ordem]

            # Renomear a 1a coluna
            df.columns = ['item', 'chk', 'ttm'] + list(df.columns[3:])

            # Adicionando a primeira coluna com o ativo
            df.insert(0,'ativo', self.ativo)

        return df
    
    def processar_dataframe(self,  df):
        for index, row in df.iterrows():
            item = row['item']
            chk = row['chk']
            ttm = row['ttm']
        
        # Criando o dicionário de anos
        anos = {int(ano): row[ano] for ano in df.columns if ano.isdigit()}
        return item, chk, ttm, anos


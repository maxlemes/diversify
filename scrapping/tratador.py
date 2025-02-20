import hashlib
import re

import pandas as pd


class TratadorDeDados:
    def __init__(self, ativo, dict_dados):
        """Inicializa a classe de tratamento dos dados."""
        self.ativo = ativo
        self.tipo_dados = next(iter(dict_dados))
        self.dados = dict_dados[self.tipo_dados]

    def criar_dataframe(self):
        """
        Cria um DataFrame a partir de uma tabela processada.
        A função processa o cabeçalho e as linhas da tabela, tratando casos em que
        cada linha pode ser uma única linha ou uma lista com duas linhas.

        Retorna:
            pd.DataFrame: DataFrame com os dados processados.
        """

        # Criar uma lista vazia para armazenar as linhas
        dados = []

        # Processa cada linha da tabela, começando da linha 1
        for i in range(1, len(self.dados)):
            linha = self.dados[i]

            if len(linha) > 1:
                linha_processada = self.processar_linha(linha)

                # Verificar se linha_processada é uma lista com uma ou duas linhas
                if isinstance(linha_processada[0], list):
                    dados.extend(
                        linha_processada
                    )  # Se for uma lista de listas, adiciona ambas as linhas
                else:
                    dados.append(
                        linha_processada
                    )  # Caso contrário, adiciona apenas uma linha

        # Processa o cabeçalho
        names = self.processar_cabecalho(self.dados[0], len(linha_processada))

        # Criar o DataFrame com as linhas processadas
        df = pd.DataFrame(dados, columns=names)

        # altera o nome da 1a coluna
        df.columns.values[0] = "item"

        # Criando a coluna 'check'
        df["chk"] = "d" + df.apply(self.calcular_checksum, axis=1)

        # colocando a coluna 'chk' na segunda posicao
        colunas = df.columns.tolist()  # Obter a lista de colunas
        colunas.remove("chk")  # Remover 'chk' da lista
        colunas.insert(1, "chk")  # Inserir 'chk' na segunda posição
        df = df[colunas]  # Reorganizar o DataFrame com a nova ordem de colunas

        for coluna in ["TTM", "Atual"]:
            if coluna in df.columns:
                colunas = df.columns.tolist()
                colunas.remove(coluna)  # Remover 'chk' da lista
                colunas.insert(2, coluna)  # Inserir 'chk' na segunda posição
                df = df[colunas]  # Reorganizar o DataFrame com a nova ordem de colunas
                df.columns = (
                    df.columns.str.lower()
                )  # converter todos os nomes das colunas para minúsculas

        # Adicionando a primeira coluna com o ativo
        df.insert(0, "ativo", self.ativo)

        # Substituindo valores ausentes (NaN) nas colunas de anos e ttm por None
        # Tratamento de anos
        anos_cols = [col for col in df.columns if col.startswith("ano_")]
        for col in anos_cols:
            df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

        return df

    def processar_cabecalho(self, linha, nro):
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
        linha[1:2] = linha[1].split("\n")  # Divide o segundo item por '\n'

        if self.tipo_dados in ["dre", "bp", "fc", "stats"]:
            # Seleciona o primeiro item e os 6 últimos valores que estão nas posições ímpares
            linha = [linha[0]] + [item for i, item in enumerate(linha) if i % 2 != 0][
                -6:
            ]

            # eliminando o ultimo item se for tipo_dados = 'bp'
            linha = linha[:-1] if self.tipo_dados == "bp" else linha

        if self.tipo_dados in ["divs"]:
            # Seleciona o primeiro item e os 5 últimos valores
            linha = [linha[0]] + linha[-5:]

        if self.tipo_dados in ["ests", "ests_r"]:
            # Seleciona o primeiro item e os 8 últimos valores
            linha = [linha[0]] + linha[-(nro - 1) :]

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
        # elimina as duas primeiras colunas (vazias)
        linha = linha[2:]
        linha[2:3] = linha[2].split(
            "\n"
        )  # Substitui o terceiro item pela lista de duas partes

        # Remove caracteres unicode indesejados
        linha = [re.sub(r"[\u202a\u202c\u202f]", "", item) for item in linha]
        linha = [re.sub("—", "", item) for item in linha]

        if self.tipo_dados in ["dre", "bp", "fc"]:
            if len(linha) <= 10:
                linha = linha[:1] + linha[2:-1]  # Eliminar o 2º e o último item
                linha = [linha[0]] + [
                    self.converter_valor(valor) for valor in linha[1:]
                ]
                return linha  # Retorna a linha processada
            else:
                linha_res = [item for i, item in enumerate(linha) if i % 2 == 0]
                linha_res = [linha_res[0]] + [
                    self.converter_valor(valor) for valor in linha_res[1:]
                ]

                # eliminando o ultimo item se for tipo_dados = 'bp'
                linha_res = linha_res[:-1] if self.tipo_dados == "bp" else linha_res

                linha_cres = [item for i, item in enumerate(linha) if i % 2 != 0]
                linha_cres = [linha_cres[0]] + [
                    (
                        self.converter_valor(valor) / 100
                        if self.converter_valor(valor) is not None
                        else None
                    )
                    for valor in linha_cres[1:]
                ]

                if linha_cres:
                    linha_cres[0] = "Cresc. " + linha_res[0]

                return [linha_res, linha_cres]

        if self.tipo_dados in ["divs", "stats"]:
            linha = linha[:1] + linha[2:]  # Eliminar o 2º elemento

            # eliminando o ultimo item se for tipo_dados = 'stats'
            linha = linha[:-1] if self.tipo_dados == "stats" else linha

            linha = [linha[0]] + [self.converter_valor(valor) for valor in linha[1:]]
            return linha  # Retorna a linha processada

        if self.tipo_dados in ["ests", "ests_r"]:
            linha = linha[:1] + linha[2:]  # Eliminar o 2º elemento
            if linha[0] == "Surpresa":
                linha = [linha[0]] + [
                    (
                        self.converter_valor(valor) / 100
                        if self.converter_valor(valor) is not None
                        else None
                    )
                    for valor in linha[1:]
                ]
            else:
                linha = [linha[0]] + [
                    self.converter_valor(valor) for valor in linha[1:]
                ]

            # Diferenciando EPS de Receita
            if self.tipo_dados in ["ests"]:
                linha[0] = "EPS - " + linha[0]
            else:
                linha[0] = "Receita - " + linha[0]

        return linha

    @staticmethod
    def converter_valor(valor):
        """
        Converte valores monetários em strings para números:
        - 'T' (trilhão) - multiplica por 1e12
        - 'B' (bilhão) → multiplica por 1e9
        - 'M' (milhão) → multiplica por 1e6
        - 'K' (milhar) → multiplica por 1e3

        Parâmetros:
            valor (str): O valor a ser convertido.

        Retorna:
            float: O valor convertido em número.
        """
        if isinstance(valor, str):  # Garante que é uma string
            valor = valor.replace(",", ".")  # Troca vírgula por ponto
            valor = valor.replace(
                ".", "", valor.count(".") - 1
            )  # elimina '.', exceto o ultimo
            valor = valor.replace("−", "-")  # Fix Unicode minus (U+2212)
            valor = valor.replace("%", "")  # remove os simbolos de %

            if valor.endswith("T"):
                return float(valor[:-1]) * 1e12
            elif valor.endswith("B"):
                return float(valor[:-1]) * 1e9
            elif valor.endswith("M"):
                return float(valor[:-1]) * 1e6
            elif valor.endswith("K"):
                return float(valor[:-1]) * 1e3
        return (
            float(valor) if valor else None
        )  # Retorna como está se não for uma string conversível

    # Função para calcular um hash SHA-256 a partir das 6 últimas colunas
    @staticmethod
    def calcular_checksum(row):
        valores = (
            row.fillna("").astype(str).tolist()
        )  # Converte valores da linha para strings
        hash_input = "".join(
            valores
        ).encode()  # Junta tudo em uma string e converte para bytes
        hash_result = hashlib.sha256(hash_input).hexdigest()[
            :10
        ]  # Usa os 10 primeiros caracteres do hash

        return hash_result

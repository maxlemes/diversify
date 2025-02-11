# diversify/empresas.py

class Empresa:
    lista = [] # Lista para armazenar as instâncias
    
    def __init__(self, nome: str, ticker: str, setor: str, subsetor: str, descricao: str, pais: str = "Brasil"):
        """Inicializa uma empresa com nome, código da ação, setor, subsetor, descrição e país."""
        self.nome = nome
        self.ticker = ticker.upper()  # Converte para maiúsculas
        self.setor = setor
        self.subsetor = subsetor
        self.descricao = descricao
        self.pais = pais
        Empresa.lista.append(self)  # Adiciona a instância na lista ao ser criada


    def __repr__(self):
        """Representação da empresa para debug."""
        return (f"Empresa(nome='{self.nome}', ticker='{self.ticker}', setor='{self.setor}', "
                f"subsetor='{self.subsetor}', pais='{self.pais}', descricao='{self.descricao[:30]}...')")

    def info(self):
        """Exibe os detalhes da empresa."""
        return (f"{self.nome} ({self.ticker}) - Setor: {self.setor}, "
                f"Subsetor: {self.subsetor}, País: {self.pais}\n"
                f"Descrição: {self.descricao}")

# empresas.py
from diversify.empresa import Empresa

# Criando as instâncias das empresas

bbas3 = Empresa(
    "Banco do Brasil S.A.", "BBAS3", "Financeiro", "Bancos",
    "O Banco do Brasil é um dos maiores bancos do país, oferecendo serviços financeiros "
    "como crédito, investimentos e seguros.",
)

cmig4 = Empresa(
    "Companhia Energética de Minas Gerais S.A.", "CMIG4", "Utilidades", "Energia Elétrica",
    "A Cemig é uma das maiores empresas do setor de energia elétrica no Brasil, atuando em geração, transmissão e distribuição.",
)

egie3 = Empresa(
    "Engie Brasil Energia S.A.", "EGIE3", "Utilidades", "Energia Elétrica",
    "A Engie é uma das maiores empresas privadas do setor de energia do Brasil, focada em geração e distribuição de energia elétrica.",
)

eztc3 = Empresa(
    "Ezetec S.A.", "EZTC3", "Consumo Cíclico", "Construção Civil",
    "A Ezetec é uma das maiores incorporadoras do Brasil, com foco no desenvolvimento de empreendimentos imobiliários.",
)

fesa4 = Empresa(
    "Ferbasa S.A.", "FESA4", "Materiais Básicos", "Mineradora",
    "A Ferbasa é a maior produtora de ferroligas do Brasil, atuando principalmente na produção de ferro-liga e outros metais.",
)

itsa3 = Empresa(
    "Itaúsa S.A.", "ITSA3", "Financeiro", "Holding",
    "A Itaúsa é uma holding de investimentos que tem participação em grandes empresas do Brasil, como o Itaú Unibanco.",
)

klbn4 = Empresa(
    "Klabin S.A.", "KLBN4", "Bens Industriais", "Papel e Celulose",
    "A Klabin é uma das maiores empresas de papel e celulose do Brasil, com foco na produção de papéis e embalagens.",
)

leve3 = Empresa(
    "Mahle Metal Leve S.A.", "LEVE3", "Consumo Cíclico", "Peças de Automóveis",
    "A Mahle Metal Leve fabrica componentes para motores e filtros, fornecendo para "
    "a indústria automotiva global.",
)

petr4 = Empresa(
    "Petróleo Brasileiro S.A. - Petrobras", "PETR4", "Petróleo, Gás e Biocombustíveis",
    "Exploração, Refino e Distribuição",
    "A Petrobras é uma das maiores empresas de energia do mundo, atuando na exploração, "
    "produção e refino de petróleo e gás natural.",
)

prio3 = Empresa(
    "Prio S.A.", "PRIO3", "Petróleo, Gás e Biocombustíveis", "Exploração e Produção",
    "A Prio é uma empresa brasileira do setor de petróleo e gás, especializada na exploração e produção de petróleo no Brasil.",
)

sabesp = Empresa(
    "Companhia de Saneamento Básico do Estado de São Paulo", "SBSP3", "Utilidades", "Saneamento",
    "A Sabesp é uma das maiores empresas de saneamento do Brasil, oferecendo serviços de água e esgoto no Estado de São Paulo.",
)

simh3 = Empresa(
    "Simpar S.A.", "SIMH3", "Consumo Cíclico", "Logística",
    "A Simpar é uma empresa brasileira que atua em diversos segmentos, como mobilidade, logística e infraestrutura.",
)

slce3 = Empresa(
    "SLC Agrícola S.A.", "SLCE3", "Consumo Não Cíclico", "Agronegócio",
    "A SLC Agrícola é uma das maiores empresas do Brasil no setor agrícola, com foco na produção de grãos como soja e milho.",
)

suza3 = Empresa(
    "Suzano Papel e Celulose S.A.", "SUZB3", "Bens Industriais", "Papel e Celulose",
    "A Suzano é uma das maiores produtoras de celulose e papel do Brasil, com forte presença no mercado global.",
)

tupy3 = Empresa(
    "Tupy S.A.", "TUPY3", "Bens Industriais", "Fundição e Peças Automotivas",
    "A Tupy é uma empresa brasileira líder no setor de fundição, especializada na produção de componentes para a indústria automotiva.",
)

vivo = Empresa(
    "Vivo S.A.", "VIVT3", "Telecomunicações", "Operadora de Telefonia",
    "A Vivo é a maior operadora de telefonia do Brasil, oferecendo serviços de telefonia móvel e fixa, além de internet e TV a cabo.",
)

wege3 = Empresa(
    "WEG S.A.", "WEGE3", "Bens de Capital", "Máquinas e Equipamentos",
    "A WEG é uma multinacional brasileira que fabrica equipamentos eletroeletrônicos, "
    "como motores elétricos, geradores e transformadores.",
)


def lista_empresas():
    lista = []
    
    for empresa in Empresa.lista:
          ticker = empresa.ticker.lower()
          lista.append(ticker)

    return lista

# Diversify: Ferramenta de Análise de Carteira de Investimentos

`Diversify` é uma aplicação em Python para análise de portfólios de investimentos, focada em ações e fundos imobiliários (FIIs) do mercado brasileiro. A ferramenta permite a importação de transações, o cálculo de posições, a análise de risco baseada em volatilidade e a geração de recomendações de rebalanceamento utilizando a estratégia de Paridade de Risco (Risk Parity).

## ✅ Principais Funcionalidades

- **Download de Dados da B3**: Automatiza o download das composições de índices (IBOV, IFIX, SMLL, IDIV) diretamente do site da B3 usando Selenium.
- **Coleta de Dados Históricos**: Utiliza a API do `yfinance` para baixar o histórico de cotações de todos os ativos da carteira.
- **Armazenamento Robusto**: Persiste todos os dados em um banco de dados SQLite, utilizando SQLAlchemy ORM para modelagem e acesso seguro.
- **Cálculo de Posição**: Consolida todas as transações de compra e venda para calcular a posição atual, quantidade e preço médio de cada ativo.
- **Análise de Risco (Volatilidade)**: Calcula a volatilidade anualizada de cada ativo, um indicador chave para a gestão de risco.
- **Alocação Inteligente (Risk Parity)**: Gera uma alocação de portfólio sugerida com base na Paridade de Risco, buscando equilibrar a contribuição de cada ativo ao risco total da carteira.
- **Plano de Rebalanceamento**: Compara a alocação atual com a sugerida e gera um plano de ordens de compra e venda para rebalancear a carteira.
- **Sugestão de Aportes**: Gera um plano de alocação otimizado para novos aportes financeiros.

## 🏗️ Arquitetura do Projeto

O projeto segue uma arquitetura em camadas para garantir a separação de responsabilidades, facilitando a manutenção e a escalabilidade.

diversify/
├── data/                     # Armazena CSVs baixados e outros dados temporários
├── drivers/                  # Contém os webdrivers (ex: geckodriver)
├── diversify/                # O pacote principal da aplicação (código fonte)
│   ├── __init__.py
│   ├── b3_services.py        # Lógica de negócio para interagir com a B3 (Selenium)
│   ├── quotes_services.py    # Lógica de negócio para cotações (yfinance)
│   └── database/
│       ├── __init__.py
│       ├── models.py         # Definição das tabelas do banco (SQLAlchemy)
│       └── repositories.py   # Padrão Repository para acesso ao banco de dados
├── tasks/                    # Scripts executáveis para tarefas específicas
│   ├── b3_insert_db.py       # insere os dados dos índices no banco
│   └── quotes_update.py      # baixa as cotacoes na B3
├── .venv/                    # Ambiente virtual Python
├── diversify.db              # Banco de dados principal
├── .gitignore
├── .pre-commit-config.yaml
├── README.md                 # Este arquivo
└── requirements.txt

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.11+
- **Banco de Dados**: SQLite com SQLAlchemy ORM
- **Análise de Dados**: Pandas & NumPy
- **Coleta de Dados**:
    - Web Scraping: Selenium & webdriver-manager
    - API de Mercado: yfinance
- **Qualidade de Código**: pre-commit, black, isort
- **Ambiente**: Python venv

## 🚀 Instalação e Setup

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

**1. Clonar o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd diversify
```

2. Criar e Ativar o Ambiente Virtual

```Bash
# Criar o ambiente
python3 -m venv .venv

# Ativar no Linux/macOS
source .venv/bin/activate
```

3. Instalar as Dependências

Bash
￼
pip install -r requirements.txt
4. Configurar o WebDriver (Firefox)
Este projeto usa o Firefox para automação. É necessário baixar o geckodriver manualmente para evitar problemas de limite de API do GitHub.

Baixe a versão mais recente do geckodriver para Linux.

Descompacte o arquivo.

Crie a pasta drivers na raiz do projeto.

Mova o executável geckodriver para dentro da pasta drivers/.

5. Configurar os Hooks de Qualidade de Código
O pre-commit garante que o código siga os padrões de formatação antes de cada commit.

Bash
￼
pre-commit install
⚙️ Como Usar
A aplicação foi projetada para ser executada em etapas.

Etapa 1: Setup Inicial do Banco de Dados
Este passo deve ser executado apenas uma vez, ou quando a composição dos índices da B3 mudar (Janeiro, Maio, Setembro).

O script inicializar_mercado.py irá:

Baixar os arquivos CSV de composição dos índices da B3.

Popular a tabela de ativos com base nesses arquivos.

Baixar 5 anos de histórico de cotações para todos os ativos cadastrados.

Bash
￼
python inicializar_mercado.py
Atenção: Este processo pode levar vários minutos, pois envolve o download de milhares de registros de dados.

Etapa 2: Manter os Dados Atualizados
Para manter os dados de cotações sempre atualizados, você pode rodar a tarefa de coleta de histórico periodicamente.

(Esta tarefa ainda pode ser criada, mas a lógica está em inicializar_mercado.py)

Etapa 3: Executar Análises
Para usar a lógica de negócio, você pode criar scripts que importem e utilizem o PortfolioService.

Exemplo de uso em um script Python:

Python
￼
from db_nexus import DatabaseSessionManager
from diversify.services import PortfolioService

# Conecta ao banco de dados
DB_URL = "sqlite:///data/portfolio.db"
session_manager = DatabaseSessionManager(DB_URL)
service = PortfolioService(session_manager)

# Gera o plano de rebalanceamento
plano = service.gerar_plano_rebalanceamento_capital_neutro()

# Imprime o plano
import pprint
pprint.pprint(plano)
🗺️ Roadmap Futuro
[ ] Criar um dashboard interativo com Streamlit ou Dash.

[ ] Desenvolver uma interface para adicionar transações manualmente.

[ ] Implementar mais métricas de análise (Sharpe Ratio, Sortino Ratio).

[ ] Adicionar suporte a outras classes de ativos (Renda Fixa, Cripto).

📄 Licença
Este projeto está licenciado sob a Licença MIT.

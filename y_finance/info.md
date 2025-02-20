A função `yf.Ticker()` do Yahoo Finance permite acessar uma ampla gama de informações sobre um ativo financeiro. Aqui estão algumas das principais opções disponíveis:

### 1. **Informações Gerais**
   - `ticker.info` → Retorna um dicionário com informações gerais da empresa.
   - `ticker.history(period="1mo")` → Retorna o histórico de preços do ativo (exemplo para 1 mês).
   - `ticker.actions` → Exibe eventos como dividendos e splits.

### 2. **Dados Financeiros**
   - `ticker.financials` → Demonstração de resultados (income statement).
   - `ticker.balance_sheet` → Balanço patrimonial.
   - `ticker.cashflow` → Fluxo de caixa.

### 3. **Dividendos e Splits**
   - `ticker.dividends` → Histórico de dividendos pagos.
   - `ticker.splits` → Histórico de splits de ações.

### 4. **Opções e Derivativos**
   - `ticker.options` → Lista datas de vencimento de opções.
   - `ticker.option_chain(date="YYYY-MM-DD")` → Retorna opções de compra e venda para uma data específica.

### 5. **Preço Atual e Estatísticas**
   - `ticker.fast_info` → Informações rápidas, como preço atual e volume.
   - `ticker.recommendations` → Recomendações de analistas.
   - `ticker.sustainability` → Informações ESG (Ambiental, Social e Governança).

Essas são algumas das opções mais utilizadas. Precisa de mais alguma informação específica?



A chave `.keys()` do dicionário retornará uma lista com todas as chaves do dicionário. Aqui está uma explicação do significado de cada uma delas:

### **1. Informações básicas da empresa**
- `address1`, `city`, `state`, `zip`, `country` → Endereço da empresa.
- `phone` → Número de telefone.
- `website` → Site oficial da empresa.
- `industry`, `industryKey`, `industryDisp` → Setor da indústria em que a empresa atua.
- `sector`, `sectorKey`, `sectorDisp` → Setor econômico da empresa.
- `longBusinessSummary` → Descrição detalhada das atividades da empresa.
- `fullTimeEmployees` → Número de funcionários da empresa.

### **2. Informações sobre a equipe executiva**
- `companyOfficers` → Lista com informações sobre os diretores e executivos da empresa.

### **3. Riscos e governança corporativa**
- `auditRisk`, `boardRisk`, `compensationRisk`, `shareHolderRightsRisk`, `overallRisk` → Indicadores de risco relacionados à governança corporativa.
- `governanceEpochDate` → Data de referência para os dados de governança.

### **4. Indicadores de preço e mercado**
- `previousClose`, `open`, `dayLow`, `dayHigh` → Preço de fechamento, abertura, mínima e máxima do dia.
- `regularMarketPreviousClose`, `regularMarketOpen`, `regularMarketDayLow`, `regularMarketDayHigh` → Versões regulares dos preços de mercado.
- `priceHint` → Precisão dos preços (número de casas decimais usadas).
- `dividendRate`, `dividendYield`, `exDividendDate`, `payoutRatio`, `fiveYearAvgDividendYield` → Indicadores de dividendos.
- `beta` → Medida de volatilidade do ativo em relação ao mercado.
- `trailingPE`, `forwardPE` → Preço sobre lucro (P/L) passado e futuro.
- `volume`, `regularMarketVolume`, `averageVolume`, `averageVolume10days`, `averageDailyVolume10Day` → Volume de negociações.

### **5. Informações financeiras**
- `marketCap` → Valor de mercado da empresa.
- `enterpriseValue` → Valor da empresa incluindo dívida líquida.
- `profitMargins` → Margem de lucro.
- `floatShares`, `sharesOutstanding`, `impliedSharesOutstanding` → Número de ações disponíveis para negociação.
- `heldPercentInsiders`, `heldPercentInstitutions` → Percentual de ações detidas por insiders e instituições.
- `bookValue`, `priceToBook` → Valor patrimonial por ação e relação preço/valor patrimonial.
- `totalRevenue`, `revenuePerShare` → Receita total e receita por ação.
- `earningsQuarterlyGrowth`, `netIncomeToCommon` → Crescimento dos lucros e lucro líquido.

### **6. Indicadores operacionais**
- `ebitda`, `totalDebt` → EBITDA e dívida total.
- `quickRatio`, `currentRatio` → Indicadores de liquidez.
- `debtToEquity` → Relação dívida/patrimônio.
- `returnOnAssets`, `returnOnEquity` → Retorno sobre ativos e sobre o patrimônio.
- `grossProfits`, `freeCashflow`, `operatingCashflow` → Lucro bruto, fluxo de caixa livre e operacional.
- `earningsGrowth`, `revenueGrowth` → Crescimento dos lucros e das receitas.
- `grossMargins`, `ebitdaMargins`, `operatingMargins` → Margens bruta, EBITDA e operacional.

### **7. Informações de mercado**
- `currency` → Moeda da cotação (BRL).
- `tradeable` → Se o ativo pode ser negociado.
- `52WeekChange`, `SandP52WeekChange`, `fiftyTwoWeekLow`, `fiftyTwoWeekHigh` → Variações e extremos da ação nos últimos 52 semanas.
- `enterpriseToRevenue`, `enterpriseToEbitda` → Indicadores financeiros de valuation.

### **8. Recomendações e expectativas**
- `targetHighPrice`, `targetLowPrice`, `targetMeanPrice`, `targetMedianPrice` → Previsões de preço-alvo por analistas.
- `recommendationMean`, `recommendationKey`, `numberOfAnalystOpinions` → Média de recomendação e número de analistas.

### **9. Dados de dividendos**
- `lastDividendValue`, `lastDividendDate` → Último dividendo pago e sua data.

### **10. Informações gerais do ativo**
- `symbol` → Código da ação.
- `exchange` → Bolsa de valores onde o ativo é negociado.
- `market` → Mercado de atuação (ex: `br_market` para Brasil).
- `shortName`, `longName` → Nome curto e nome completo da empresa.

Essa é uma visão geral dos principais campos e seus significados. Alguma informação específica que você quer explorar melhor?



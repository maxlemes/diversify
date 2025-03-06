def calcular_percentuais_atuais(df):
    total_investido = df["valor"].sum()
    df["percentual"] = (df["valor"] / total_investido) * 100
    percentuais = dict(zip(df["classe_ativo"], df["percentual"]))
    return percentuais

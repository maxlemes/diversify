import streamlit as st


def show_sidebar():
    #    st.sidebar.title("Investimentos")

    # 🟢 Quadro: Investimento Atual
    st.sidebar.subheader("Investimento Atual (R$)")
    investimentos = {
        "Renda Fixa": st.sidebar.number_input(
            "Renda Fixa (R$)", min_value=0.0, format="%.2f"
        ),
        "Ações": st.sidebar.number_input("Ações (R$)", min_value=0.0, format="%.2f"),
        "FIIs": st.sidebar.number_input("FIIs (R$)", min_value=0.0, format="%.2f"),
        "Fundos de Previdência": st.sidebar.number_input(
            "Fundos de Previdência (R$)", min_value=0.0, format="%.2f"
        ),
        "Criptomoedas": st.sidebar.number_input(
            "Criptomoedas (R$)", min_value=0.0, format="%.2f"
        ),
        "Investimentos no Exterior": st.sidebar.number_input(
            "Investimentos no Exterior (R$)", min_value=0.0, format="%.2f"
        ),
    }

    st.sidebar.divider()  # Linha separadora

    # 🔵 Campo: Aporte
    st.sidebar.subheader("Aporte")
    aporte = st.sidebar.number_input(
        "Valor do Aporte (R$)", min_value=0.0, format="%.2f"
    )

    st.sidebar.divider()  # Linha separadora

    # 🔴  Quadro: Distribuição Desejada (Percentual)
    st.sidebar.subheader("Distribuição Desejada (%)")
    distribuicao = {
        "Renda Fixa": st.sidebar.number_input(
            "Renda Fixa (%)", min_value=0, max_value=100, value=40
        ),
        "Ações": st.sidebar.number_input(
            "Ações (%)", min_value=0, max_value=100, value=30
        ),
        "FIIs": st.sidebar.number_input(
            "FIIs (%)", min_value=0, max_value=100, value=10
        ),
        "Fundos de Previdência": st.sidebar.number_input(
            "Fundos de Previdência (%)", min_value=0, max_value=100, value=10
        ),
        "Criptomoedas": st.sidebar.number_input(
            "Criptomoedas (%)", min_value=0, max_value=100, value=5
        ),
        "Investimentos no Exterior": st.sidebar.number_input(
            "Investimentos no Exterior (%)",
            min_value=0,
            max_value=100,
            value=5,
        ),
    }

    return investimentos, aporte, distribuicao

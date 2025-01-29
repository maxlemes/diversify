import streamlit as st
from graficos import criar_grafico, grafico_comparativo
import plotly.colors  # Importando a biblioteca de cores do Plotly

def show_main_content(investimentos, aporte, distribuicao):
  #  st.title("Dashboard de Análise de Empresas")

    # 📌 Calcular Investimentos, Aporte e Patrimônio Total
    investimentos_total = sum(investimentos.values())
    aporte_total = aporte
    patrimonio_total = investimentos_total + aporte_total

    # 📌 Exibir Patrimônio de forma destacada
    st.markdown(f"""
   <h1 style="text-align: center; color: #d3d3d3;">
       Patrimônio Total: <span style="color: #1e88e5; font-size: 40px; font-weight: bold;">R$ {patrimonio_total:,.2f}</span>
    </h1>
    """, unsafe_allow_html=True)

    # 📌 Exibir as 3 informações com formatação
    st.markdown(f"""
    <div style="text-align: center; font-size: 25px;">
    <p>
       <span style="margin-right: 50px;"><strong>Valor Investido:</strong> <span style="color: #4caf50;">R$ {investimentos_total:,.2f}</span></span>
       <span><strong>Aporte:</strong> <span style="color: #4caf50;">R$ {aporte_total:,.2f}</span></span>
   </p>
   </div>
   """, unsafe_allow_html=True)


     # 📌 Exibir gráficos lado a lado
    col1, col2 = st.columns(2)  # Cria 2 colunas para os gráficos

    # Gerar paleta de cores azuis
    cores_padrao = plotly.colors.qualitative.Plotly  # Usa a paleta padrão do Plotly para gráficos qualitativos

    # Gráfico de rosca para os investimentos
    with col1:
        fig1 = criar_grafico('rosca', {ativo: (valor / investimentos_total) * 100 for ativo, valor in investimentos.items()},
                             "Distribuição Atual", cores_padrao)
        st.markdown("<h3 style='text-align: center;'>Distribuição Atual</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig1)  # Exibe o gráfico de rosca

     # Gráfico de rosca para a distribuição desejada
    with col2:
        fig2 = criar_grafico('rosca', distribuicao, "Distribuição Desejada", cores_padrao)
        st.markdown("<h3 style='text-align: center;'>Distribuição Desejada</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig2)  # Exibe o gráfico de rosca

    # 📌 Calcular valores reais para distribuição desejada e atual
    distribuicao_atual = {ativo: valor for ativo, valor in investimentos.items()}
    distribuicao_desejada = {ativo: (patrimonio_total * percentual / 100) for ativo, percentual in distribuicao.items()}

    # Gerar o gráfico comparativo
    fig_comparativo = grafico_comparativo(distribuicao_atual, distribuicao_desejada, "Distribuição Atual vs. Desejada")

    # Exibir o gráfico no Streamlit
    st.markdown("<h3 style='text-align: center;'>Distribuição Atual vs Distribuição Desejada</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_comparativo)

    # Calcular a diferença em valores absolutos entre a distribuição atual e a desejada
    diferencias = {
        ativo: (distribuicao_desejada.get(ativo, 0) - distribuicao_atual.get(ativo, 0))
        for ativo in distribuicao_atual
    }

    # Identificar o ativo com a maior diferença
    maior_diferenca_ativo = max(diferencias, key=diferencias.get)
    maior_diferenca_valor = diferencias[maior_diferenca_ativo]

    # Exibir a recomendação do ativo mais atrasado
    if maior_diferenca_ativo:
       st.markdown(f"""
       <div style="font-size: 24px; color: #d3d3d3;">
           Sugestão de Aporte: <strong>{maior_diferenca_ativo}</strong>. O valor atual está
           <span style="color: #ff5722;">R$ {maior_diferenca_valor:,.2f}</span> abaixo do valor desejado.
       </div>
       """, unsafe_allow_html=True)
    else:
       st.markdown("""
       <div style="font-size: 24px; color: #d3d3d3;">
           Todos os investimentos estão de acordo com a distribuição desejada.
       </div>
       """, unsafe_allow_html=True)


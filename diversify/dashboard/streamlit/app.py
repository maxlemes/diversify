import streamlit as st
from main_content import show_main_content
from sidebar import show_sidebar

st.set_page_config(layout="wide")

# Captura os investimentos e a distribuição desejada
investimentos, aporte, distribuicao = show_sidebar()

# Passa os dados para o conteúdo principal
show_main_content(investimentos, aporte, distribuicao)

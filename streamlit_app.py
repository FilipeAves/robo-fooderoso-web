
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Robô Fooderoso da Cotação", layout="wide")

st.title("🤖 Robô Fooderoso da Cotação")
st.write("Preencha os dados abaixo para gerar a cotação automática com base nas planilhas.")

# Dados do cliente
col1, col2 = st.columns(2)
with col1:
    cliente_codigo = st.text_input("🧾 Código do Cliente")
with col2:
    cliente_nome = st.text_input("🏷️ Nome do Cliente")

# Pedido
cotacao_texto = st.text_area("📝 Cole o texto da cotação aqui (ex: 2 cx óleo soya 900ml)", height=200)

# Upload de imagem (OCR ainda não implementado)
imagem = st.file_uploader("📷 Ou envie uma imagem com o pedido (simulado)", type=["png", "jpg", "jpeg"])

# Ação
if st.button("📄 Gerar Cotação em PDF"):
    if not cliente_codigo and not cliente_nome:
        st.warning("⚠️ Informe pelo menos o código ou nome do cliente.")
    elif not cotacao_texto and not imagem:
        st.warning("⚠️ Insira o texto da cotação ou envie uma imagem.")
    else:
        with st.spinner("Analisando cotação e gerando PDF..."):
            # Aqui será feita a lógica real no futuro
            st.success("✅ Cotação gerada com sucesso! (simulado)")
            st.markdown("🔗 Em breve: link para baixar PDF aqui.")

st.markdown("---")
st.caption("Robô Fooderoso da Cotação • Desenvolvido para Rio Quality")

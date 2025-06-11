
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Robô Fooderoso da Cotação", layout="wide")

st.title("🤖 Robô Fooderoso da Cotação")
st.write("Cole aqui o texto da cotação ou envie uma imagem com o pedido.")

# Campo de texto
cotacao_texto = st.text_area("📝 Cotação (texto)", height=200)

# Upload de imagem
imagem = st.file_uploader("📷 Ou envie uma imagem com o pedido", type=["png", "jpg", "jpeg"])

# Botão para gerar PDF (ainda simbólico)
if st.button("📄 Gerar Cotação em PDF"):
    if cotacao_texto or imagem:
        st.success("PDF gerado com sucesso! (simulado)")
    else:
        st.warning("Por favor, insira o texto ou envie uma imagem.")

st.markdown("---")
st.caption("Desenvolvido para Rio Quality • Versão básica de teste")

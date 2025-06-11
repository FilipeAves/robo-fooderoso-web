
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Robô Fooderoso da Cotação", layout="wide")

st.title("🤖 Robô Fooderoso da Cotação")
st.write("Cole abaixo o pedido do cliente ou envie uma imagem com o print do WhatsApp.")

# Área para colar o pedido
cotacao_texto = st.text_area("📝 Pedido (texto ou colado do WhatsApp)", height=200)

# Upload de imagem (apenas interface, OCR ainda não ativo)
imagem = st.file_uploader("📷 Envie imagem do pedido (print, etiqueta, etc.)", type=["png", "jpg", "jpeg"])

# Simulação de geração de PDF
if st.button("📄 Gerar Cotação em PDF"):
    if cotacao_texto or imagem:
        with st.spinner("Gerando PDF da cotação..."):
            # Simulação de análise e geração
            st.success("✅ Cotação gerada com sucesso! (PDF simulado)")
            st.markdown("🔗 Em breve: link para baixar PDF aqui.")
    else:
        st.warning("⚠️ Por favor, cole o pedido ou envie uma imagem.")

st.markdown("---")
st.caption("Versão inicial do Robô Fooderoso • Desenvolvido para Rio Quality")

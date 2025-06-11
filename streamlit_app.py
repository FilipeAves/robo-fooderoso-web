
import streamlit as st
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Robô Fooderoso da Cotação", layout="wide")
st.title("🤖 Robô Fooderoso da Cotação")
st.write("Preencha os dados abaixo para gerar a cotação automática.")

# Dados do cliente
col1, col2 = st.columns(2)
with col1:
    cliente_codigo = st.text_input("🧾 Código do Cliente")
with col2:
    cliente_nome = st.text_input("🏷️ Nome do Cliente")

# Pedido
cotacao_texto = st.text_area("📝 Cole o texto da cotação aqui (ex: 2 cx óleo soya 900ml)", height=200)

def gerar_pdf(cliente, itens):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "RIO QUALITY COMÉRCIO DE ALIMENTOS S/A", 0, 1, "C")
            self.set_font("Arial", "", 10)
            self.cell(0, 8, "Cotação Gerada pelo Robô Fooderoso", 0, 1, "C")
            self.ln(5)
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")
        def add_cotacao(self, cliente, produtos):
            self.set_font("Arial", "", 10)
            self.cell(0, 10, f"Cliente: {cliente}", ln=True)
            self.ln(5)
            for produto in produtos:
                self.cell(0, 8, f"- {produto}", ln=True)

    pdf = PDF()
    pdf.add_page()
    pdf.add_cotacao(cliente, itens)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_path.name)
    return temp_path.name

# Ação
if st.button("📄 Gerar Cotação em PDF"):
    if not cliente_codigo and not cliente_nome:
        st.warning("⚠️ Informe o código ou nome do cliente.")
    elif not cotacao_texto:
        st.warning("⚠️ Insira o texto da cotação.")
    else:
        cliente = f"{cliente_codigo} - {cliente_nome}".strip(" -")
        itens = [linha.strip() for linha in cotacao_texto.split("\n") if linha.strip()]
        caminho_pdf = gerar_pdf(cliente, itens)
        with open(caminho_pdf, "rb") as f:
            st.success("✅ Cotação gerada com sucesso!")
            st.download_button(
                label="📥 Baixar Cotação em PDF",
                data=f,
                file_name="cotacao_robo_fooderoso.pdf",
                mime="application/pdf"
            )
        os.unlink(caminho_pdf)

st.markdown("---")
st.caption("Robô Fooderoso da Cotação • Desenvolvido para Rio Quality")

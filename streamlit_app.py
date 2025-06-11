
import streamlit as st
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Robô Fooderoso da Cotação", layout="wide")
st.title("🤖 Robô Fooderoso da Cotação")
st.write("Preencha os dados abaixo para gerar a cotação no formato Rio Quality.")

# Dados do cliente
col1, col2 = st.columns(2)
with col1:
    cliente_codigo = st.text_input("🧾 Código do Cliente")
with col2:
    vendedor_nome = st.text_input("🧑‍💼 Nome do Vendedor")

cotacao_texto = st.text_area("📝 Cole o texto da cotação aqui (Ex: 2 cx Óleo Soya 900ml 7,72)", height=250)

class PDFCotacao(FPDF):
    def header(self):
        self.set_font("Arial", "B", 10)
        self.multi_cell(0, 5, "RIO QUALITY COMÉRCIO DE ALIMENTOS S/A\nRua Embaú, 2207 - Pavuna / Parque Columbia\nCEP: 21535-000 - Rio de Janeiro / RJ\nCNPJ: 08.969.770/0001-59   IE: 78.369.213   Tel: (21) 3544-4848   Fax: (21) 3451-7462", 0, "C")
        self.ln(2)
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")
    def add_cotacao_detalhada(self, cliente, vendedor, produtos):
        self.set_font("Arial", "", 10)
        self.cell(0, 8, f"Cliente: {cliente}", ln=True)
        self.cell(0, 8, f"Vendedor: {vendedor}", ln=True)
        self.ln(5)
        self.set_font("Arial", "B", 9)
        self.cell(70, 8, "Produto", 1)
        self.cell(30, 8, "Embalagem", 1)
        self.cell(20, 8, "Qtde", 1, 0, "C")
        self.cell(30, 8, "Valor Unit.", 1, 0, "R")
        self.cell(30, 8, "Total", 1, 1, "R")
        self.set_font("Arial", "", 9)
        total_geral = 0
        for prod in produtos:
            nome, emb, qtde, unit = prod
            total = float(qtde) * float(unit)
            total_geral += total
            self.cell(70, 8, nome, 1)
            self.cell(30, 8, emb, 1)
            self.cell(20, 8, str(qtde), 1, 0, "C")
            self.cell(30, 8, f"R$ {unit:,.2f}".replace(".", ","), 1, 0, "R")
            self.cell(30, 8, f"R$ {total:,.2f}".replace(".", ","), 1, 1, "R")
        self.set_font("Arial", "B", 10)
        self.cell(150, 8, "TOTAL GERAL DA COTAÇÃO", 1)
        self.cell(30, 8, f"R$ {total_geral:,.2f}".replace(".", ","), 1, 1, "R")

def gerar_pdf(cliente, vendedor, texto):
    produtos = []
    for linha in texto.split("\n"):
        partes = linha.strip().split()
        if len(partes) >= 4:
            try:
                qtde = float(partes[0])
                emb = partes[1]
                valor = float(partes[-1].replace(",", "."))
                nome = " ".join(partes[2:-1])
                produtos.append((nome, emb, qtde, valor))
            except:
                continue
    pdf = PDFCotacao()
    pdf.add_page()
    pdf.add_cotacao_detalhada(cliente, vendedor, produtos)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_path.name)
    return temp_path.name

if st.button("📄 Gerar Cotação em PDF"):
    if not cliente_codigo or not vendedor_nome:
        st.warning("⚠️ Informe o código do cliente e o nome do vendedor.")
    elif not cotacao_texto:
        st.warning("⚠️ Cole o texto da cotação.")
    else:
        cliente = cliente_codigo.strip()
        vendedor = vendedor_nome.strip()
        caminho_pdf = gerar_pdf(cliente, vendedor, cotacao_texto)
        with open(caminho_pdf, "rb") as f:
            st.success("✅ Cotação gerada com sucesso!")
            st.download_button("📥 Baixar PDF da Cotação", f, file_name="cotacao_robo_fooderoso.pdf", mime="application/pdf")
        os.unlink(caminho_pdf)

st.markdown("---")
st.caption("Robô Fooderoso da Cotação • Padrão Rio Quality • Desenvolvido para uso comercial")

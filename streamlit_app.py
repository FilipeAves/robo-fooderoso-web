
import streamlit as st
from fpdf import FPDF
import tempfile
import os
import re
import pandas as pd

st.set_page_config(page_title="Robô Fooderoso da Cotação", layout="wide")
st.title("🤖 Robô Fooderoso da Cotação")

col1, col2 = st.columns(2)
with col1:
    cliente_codigo = st.text_input("Código do Cliente")
with col2:
    vendedor_manual = st.text_input("Vendedor (deixe em branco para buscar automaticamente)")

cotacao_texto = st.text_area("📝 Cole o texto da cotação", height=250)

@st.cache_data
def buscar_info_cliente(codigo):
    try:
        df = pd.read_excel("JAN-MAI-INDUSTRIA-Compactada.xlsx", sheet_name="MAI-CLIENTE-PRACAEROTA")
        dados = df[df["Cod. Cliente"] == int(codigo)][["Cod. Cliente", "Cliente", "Vendedor"]].drop_duplicates()
        if not dados.empty:
            nome = dados.iloc[0]["Cliente"]
            vendedor = dados.iloc[0]["Vendedor"]
            return nome, vendedor
    except:
        pass
    return None, None

class PDFCotacao(FPDF):
    def header(self):
        self.set_font("Arial", "B", 8)
        self.multi_cell(0, 4, "RIO QUALITY COMÉRCIO DE ALIMENTOS S/A\nRua Embaú, 2207 - Pavuna / Parque Columbia\nCEP: 21535-000 - Rio de Janeiro / RJ\nCNPJ: 08.969.770/0001-59   IE: 78.369.213   Tel: (21) 3544-4848   Fax: (21) 3451-7462", 0, "C")
        self.ln(1)
    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "I", 6)
        self.cell(0, 6, f"Página {self.page_no()}", 0, 0, "C")
    def tabela(self, titulo, itens):
        self.set_font("Arial", "B", 7)
        self.cell(66, 5, "Produto", 1)
        self.cell(24, 5, "Embalagem", 1)
        self.cell(12, 5, "Qtde", 1, 0, "C")
        self.cell(24, 5, "Unitário", 1, 0, "R")
        self.cell(24, 5, "Total", 1, 1, "R")
        self.set_font("Arial", "", 7)
        total = 0
        for nome, emb, qtde, valor in itens:
            linha = qtde * valor
            total += linha
            self.cell(66, 5, nome, 1)
            self.cell(24, 5, emb, 1)
            self.cell(12, 5, str(qtde), 1, 0, "C")
            self.cell(24, 5, f"R$ {valor:,.2f}".replace(".", ","), 1, 0, "R")
            self.cell(24, 5, f"R$ {linha:,.2f}".replace(".", ","), 1, 1, "R")
        self.set_font("Arial", "B", 8)
        self.cell(126, 5, f"TOTAL {titulo.upper()}", 1)
        self.cell(24, 5, f"R$ {total:,.2f}".replace(".", ","), 1, 1, "R")

    def gerar(self, cliente_nome, vendedor, cotacao, observacoes, sugestoes):
        self.set_font("Arial", "", 8)
        self.cell(0, 5, f"Cliente: {cliente_nome}", ln=True)
        self.cell(0, 5, f"Vendedor: {vendedor}", ln=True)
        self.ln(3)
        self.tabela("Cotação", cotacao)
        if observacoes:
            self.ln(2)
            self.set_font("Arial", "B", 7)
            self.cell(0, 5, "Observações:", ln=True)
            self.set_font("Arial", "", 7)
            for obs in observacoes:
                self.multi_cell(0, 4, f"- {obs}", 0)
        if sugestoes:
            self.ln(4)
            self.set_font("Arial", "B", 8)
            self.cell(0, 5, "Sugestões com base no histórico:", ln=True)
            self.ln(1)
            self.tabela("Sugestões", sugestoes)

def processar_texto(texto):
    itens = []
    obs = []
    for linha in texto.split("\n"):
        if not linha.strip():
            continue
        if "em falta" in linha.lower():
            obs.append(linha.strip())
            continue
        match = re.findall(r"(\d+[.,]?\d*)\s+(\w+)\s+(.+?)\s+(\d+[.,]\d{2})$", linha.strip())
        if match:
            qtde, emb, nome, val = match[0]
            itens.append((nome.strip(), emb.strip(), float(qtde.replace(",", ".")), float(val.replace(",", "."))))
        else:
            obs.append(linha.strip())
    return itens, obs

if st.button("📄 Gerar Cotação em PDF"):
    nome_cli, vend_auto = buscar_info_cliente(cliente_codigo)
    vendedor = vendedor_manual or vend_auto or "NÃO IDENTIFICADO"
    nome_cliente = f"{cliente_codigo} - {nome_cli or 'NOME NÃO ENCONTRADO'}"
    itens, obs = processar_texto(cotacao_texto)
    sugestoes = [
        ("Requeijão Cremoso 1,5kg Catupiry", "BI", 1, 56.90),
        ("Batata Palito 2,5Kg Mccain", "CX", 1, 188.00),
        ("Tilápia Congelada 5Kg Planalto", "PC", 1, 198.00),
    ]
    pdf = PDFCotacao()
    pdf.add_page()
    pdf.gerar(nome_cliente, vendedor, itens, obs, sugestoes)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            st.download_button("📥 Baixar PDF da Cotação", f, file_name="cotacao_robo_fooderoso.pdf", mime="application/pdf")


import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Robô com Debug", layout="wide")
st.title("🤖 Robô Fooderoso da Cotação (modo debug)")

col1, col2 = st.columns(2)
with col1:
    cliente_codigo = st.text_input("Código do Cliente")
with col2:
    vendedor_manual = st.text_input("Vendedor (opcional)")

cotacao_texto = st.text_area("📝 Cole o texto da cotação", height=200)

def carregar_planilhas_debug():
    debug_info = {}
    try:
        df_maio = pd.read_excel("JAN-MAI-INDUSTRIA-Compactada.xlsx", sheet_name="MAI-CLIENTE-PRACAEROTA", engine="openpyxl")
        debug_info["maio_status"] = "✅ Planilha de MAIO carregada com sucesso!"
    except Exception as e:
        df_maio = pd.DataFrame()
        debug_info["maio_status"] = f"❌ Erro ao carregar MAIO: {str(e)}"

    try:
        df_semana = pd.read_excel("TABELA DA SEMANA - 09-06 a 13-06.xlsx", engine="openpyxl")
        debug_info["semana_status"] = "✅ Tabela da semana carregada!"
    except Exception as e:
        df_semana = pd.DataFrame()
        debug_info["semana_status"] = f"❌ Erro ao carregar TABELA DA SEMANA: {str(e)}"

    return df_maio, df_semana, debug_info

if st.button("🛠 Testar carregamento de planilhas"):
    df_maio, df_semana, debug = carregar_planilhas_debug()
    st.subheader("📋 Status de carregamento:")
    for k, v in debug.items():
        st.text(f"{k}: {v}")
    if not df_maio.empty and cliente_codigo:
        try:
            info = df_maio[df_maio["Cod. Cliente"] == int(cliente_codigo)][["Cliente", "Vendedor"]].drop_duplicates()
            if not info.empty:
                nome = info.iloc[0]["Cliente"]
                vendedor = vendedor_manual or info.iloc[0]["Vendedor"]
                st.success(f"🎯 Cliente encontrado: {cliente_codigo} - {nome}")
                st.success(f"🎯 Vendedor: {vendedor}")
            else:
                st.warning("Cliente não encontrado na planilha de MAIO.")
        except Exception as e:
            st.error(f"Erro ao buscar cliente: {str(e)}")

import streamlit as st
import gspread
import pandas as pd
import json

st.set_page_config(page_title="Control Bodega MOTSUR", layout="wide")
st.title("📦 Sistema de Control de Bodega - MOTSUR")

# 1. Conexión usando Secrets
def get_data():
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1DyfKnW-JOtWDRp7OqsbyX03A1rdiMMZkIcqlq2nkofA/edit")
    return sh.worksheet("Hoja1").get_all_records()

# 2. Cargar y mostrar datos
data = get_data()
df = pd.DataFrame(data)

st.subheader("Estado Actual del Inventario")
st.dataframe(df, use_container_width=True)

# 3. Formulario simple
st.subheader("Registrar Movimiento")
with st.form("movimiento"):
    col1, col2 = st.columns(2)
    material = col1.selectbox("Material", df.iloc[:, 0].tolist())
    cantidad = col2.number_input("Cantidad", min_value=1)
    if st.form_submit_button("Actualizar"):
        st.info("Función de escritura activada. Asegúrate de que el JSON en 'Secrets' tenga permisos de Editor.")

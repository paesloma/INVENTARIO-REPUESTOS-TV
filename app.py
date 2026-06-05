import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de página
st.set_page_config(page_title="Control Bodega MOTSUR", layout="wide")
st.title("📦 Sistema de Control de Bodega")

# Conexión a Google Sheets usando gspread
# Para que esto funcione, asegúrate de que tu hoja sea pública 
# o que estés usando credenciales (esto es para lectura/escritura sencilla)
def get_data():
    # Usaremos una lógica de conexión directa
    # Nota: Si tu hoja no es pública, necesitarás un archivo JSON de credenciales
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1DyfKnW-JOtWDRp7OqsbyX03A1rdiMMZkIcqlq2nkofA/edit")
    worksheet = sh.worksheet("Hoja1")
    return pd.DataFrame(worksheet.get_all_records())

# Cargar datos
try:
    df = get_data()
    # Tu lógica original continúa aquí...
    st.dataframe(df)
    
except Exception as e:
    st.error(f"Error al conectar: {e}")

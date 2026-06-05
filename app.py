import streamlit as st
import gspread
import pandas as pd
import json

st.set_page_config(page_title="Gestión Bodega", layout="wide")
st.title("📦 Inventario Bodega MOTSUR")

# Función de conexión optimizada
def get_connection():
    # Carga el JSON desde los Secrets
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
    # Abre la hoja por URL
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1DyfKnW-JOtWDRp7OqsbyX03A1rdiMMZkIcqlq2nkofA/edit")
    return sh.worksheet("Hoja1")

# Cargar datos
ws = get_connection()
data = ws.get_all_records()
df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

# Lógica de escritura (Modificación)
st.subheader("Registrar Movimiento")
with st.form("form_registro"):
    material = st.selectbox("Material", df.iloc[:, 0].tolist())
    cantidad = st.number_input("Cantidad", min_value=1)
    accion = st.radio("Acción", ["Ingreso", "Salida"])
    submit = st.form_submit_button("Guardar Cambios")

if submit:
    # Buscar la fila (asumiendo que material está en columna 1)
    fila = df[df.iloc[:, 0] == material].index[0] + 2 # +2 para formato gspread
    stock_actual = int(df.at[fila-2, df.columns[1]])
    
    nuevo_stock = stock_actual + cantidad if accion == "Ingreso" else stock_actual - cantidad
    
    # Escribir en la hoja
    ws.update_cell(fila, 2, nuevo_stock)
    st.success(f"¡Base de datos actualizada! Nuevo stock: {nuevo_stock}")
    st.rerun()

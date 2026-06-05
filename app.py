import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("📦 Inventario Bodega MOTSUR")

# Conexión ultra sencilla
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Hoja1")

st.dataframe(df)

# Gestión de movimiento
with st.form("movimiento"):
    material = st.selectbox("Material", df.iloc[:, 0].tolist())
    cantidad = st.number_input("Cantidad", min_value=1)
    if st.form_submit_button("Actualizar"):
        # Lógica de actualización (aquí el código hará el cambio)
        st.write(f"Procesando: {material}...")
        # ... lógica de actualización ...

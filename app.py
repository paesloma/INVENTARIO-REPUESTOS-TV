import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Control Bodega MOTSUR", layout="wide")
st.title("📦 Sistema de Control de Bodega")

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar datos (Asegúrate de que el nombre de la hoja sea 'Hoja1' o cámbialo abajo)
df = conn.read(worksheet="Hoja1", usecols=[0, 1, 2]) # Ajusta las columnas según tu sheet
df = df.dropna(how="all")

# Sidebar para acciones
st.sidebar.header("Gestión de Inventario")
action = st.sidebar.radio("Seleccione Acción", ["Ver Inventario", "Ingreso Material", "Salida Material"])

if action == "Ver Inventario":
    st.subheader("Estado Actual del Stock")
    st.dataframe(df, use_container_width=True)

else:
    # Formulario para Ingreso o Salida
    with st.form("form_inventario"):
        st.subheader(action)
        item = st.selectbox("Material", df.iloc[:, 0].tolist()) # Asume columna 0 es Material
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        submit = st.form_submit_button("Confirmar")

    if submit:
        # Obtener stock actual
        idx = df.index[df.iloc[:, 0] == item][0]
        stock_actual = int(df.at[idx, df.columns[1]]) # Asume columna 1 es Stock
        
        if action == "Ingreso Material":
            nuevo_stock = stock_actual + cantidad
            df.at[idx, df.columns[1]] = nuevo_stock
            conn.update(worksheet="Hoja1", data=df)
            st.success(f"Ingreso exitoso. Nuevo stock: {nuevo_stock}")
            
        elif action == "Salida Material":
            if stock_actual >= cantidad:
                nuevo_stock = stock_actual - cantidad
                df.at[idx, df.columns[1]] = nuevo_stock
                conn.update(worksheet="Hoja1", data=df)
                st.success(f"Salida exitosa. Nuevo stock: {nuevo_stock}")
            else:
                st.error("Error: Stock insuficiente")
        
        st.rerun()

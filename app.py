import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Control de Inventario", layout="wide")
st.title("📦 Sistema de Control de Bodega")

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Inventario", usecols=[0, 1, 2], ttl=5)
df = df.dropna(how="all")

# Visualización de Inventario (Requerimiento: Siempre mostrar la tabla)
st.subheader("Estado Actual del Inventario")
st.dataframe(df, use_container_width=True)

# Visualización Gráfica (Requerimiento: Siempre generar gráfica)
st.subheader("Gráfica de Niveles de Stock")
fig = px.bar(df, x="Material", y="Stock", color="Stock", title="Stock por Artículo")
st.plotly_chart(fig, use_container_width=True)

# Acciones de Inventario
st.divider()
st.subheader("Gestión de Material")

col1, col2 = st.columns(2)

with col1:
    action = st.radio("Seleccione la acción:", ["Ingreso de Material", "Salida de Material"])

with col2:
    selected_material = st.selectbox("Seleccione el ítem:", df["Material"].tolist())
    quantity = st.number_input("Cantidad", min_value=1, step=1)
    
    if st.button("Ejecutar Operación"):
        # Lógica de actualización
        current_stock = df.loc[df["Material"] == selected_material, "Stock"].values[0]
        
        if action == "Ingreso de Material":
            new_stock = current_stock + quantity
        else:
            if current_stock >= quantity:
                new_stock = current_stock - quantity
            else:
                st.error("Stock insuficiente para esta salida.")
                new_stock = current_stock

        # Actualizar Google Sheets
        df.loc[df["Material"] == selected_material, "Stock"] = new_stock
        conn.update(worksheet="Inventario", data=df)
        st.success(f"Operación realizada. Nuevo stock: {new_stock}")
        st.rerun()

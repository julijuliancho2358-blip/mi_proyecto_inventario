# app.py
import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Dashboard de Inventario", layout="wide")
st.title("Dashboard de Gestion de Inventario")

def obtener_datos():
    try:
        response = requests.get(f"{API_URL}/productos/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.ConnectionError:
        st.error("Error: No se pudo conectar a la API. Esta corriendo FastAPI?")
        return []

with st.sidebar:
    st.header("Añadir Nuevo Producto")
    with st.form("form_crear"):
        nombre = st.text_input("Nombre del producto")
        precio = st.number_input("Precio ($)", min_value=0.0, step=0.1)
        cantidad = st.number_input("Cantidad en Stock", min_value=0, step=1)
        submit_btn = st.form_submit_button("Guardar Producto")

    if submit_btn:
        nuevo_prod = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
        res = requests.post(f"{API_URL}/productos/", json=nuevo_prod)
        if res.status_code == 200:
            st.success("Producto añadido!")
            st.rerun()
        else:
            st.error("Error al añadir producto")

productos = obtener_datos()

if productos:
    col1, col2, col3 = st.columns(3)
    df = pd.DataFrame(productos)

    col1.metric("Total de Productos", len(df))
    col2.metric("Valor Total", f"${(df['precio'] * df['cantidad']).sum():.2f}")
    col3.metric("Stock Total", df['cantidad'].sum())

    st.subheader("Lista de Productos")
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("Eliminar un Producto")
    col_del1, col_del2 = st.columns([1, 3])
    with col_del1:
        id_a_borrar = st.selectbox("ID a borrar", df['id'].tolist())
    with col_del2:
        st.write("")
        st.write("")
        if st.button("Eliminar producto", type="primary"):
            res = requests.delete(f"{API_URL}/productos/{id_a_borrar}")
            if res.status_code == 200:
                st.success(f"Producto {id_a_borrar} eliminado.")
                st.rerun()
            else:
                st.error("Error al eliminar")
else:
    st.info("El inventario esta vacio o la API no esta conectada.")
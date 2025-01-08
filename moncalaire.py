import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Configuración de la página
st.set_page_config(page_title="Monitoreo de Calidad del Aire - CDMX", layout="wide")

# Generar datos simulados
def generar_datos_simulados(n=100):
    np.random.seed(42)
    latitudes = np.random.uniform(19.2, 19.6, n)
    longitudes = np.random.uniform(-99.3, -99.0, n)
    pm25 = np.random.uniform(10, 150, n)  # Niveles de PM2.5
    pm10 = np.random.uniform(20, 200, n)  # Niveles de PM10
    co = np.random.uniform(0.5, 5, n)    # Niveles de CO
    return pd.DataFrame({
        "latitude": latitudes,
        "longitude": longitudes,
        "PM2.5": pm25,
        "PM10": pm10,
        "CO": co
    })

# Crear datos
datos = generar_datos_simulados()

# Título de la aplicación
st.title("Monitoreo de Calidad del Aire en la Ciudad de México")

# Controles para filtros
st.sidebar.header("Controles de Filtro")
pm25_max = st.sidebar.slider("Máximo PM2.5", min_value=10, max_value=150, value=100)
pm10_max = st.sidebar.slider("Máximo PM10", min_value=20, max_value=200, value=120)
co_max = st.sidebar.slider("Máximo CO (ppm)", min_value=0.5, max_value=5.0, value=3.0)

# Filtrar datos según los valores seleccionados
datos_filtrados = datos[
    (datos["PM2.5"] <= pm25_max) &
    (datos["PM10"] <= pm10_max) &
    (datos["CO"] <= co_max)
]

# Mapa interactivo con pydeck
st.subheader("Mapa de Calidad del Aire")
st.map(datos_filtrados[["latitude", "longitude"]])

# Visualización avanzada con pydeck
st.subheader("Visualización Avanzada")
layer = pdk.Layer(
    "ScatterplotLayer",
    datos_filtrados,
    get_position="[longitude, latitude]",
    get_fill_color="[PM2.5 * 2, PM10 * 1, CO * 50]",
    get_radius=200,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=19.432608,
    longitude=-99.133209,
    zoom=10,
    pitch=45,
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "PM2.5: {PM2.5}\nPM10: {PM10}\nCO: {CO}"})
st.pydeck_chart(r)

# Mostrar datos en tabla
st.subheader("Datos Filtrados")
st.dataframe(datos_filtrados)
